from flask_cors import CORS
from pyfairdatatools import __version__
import model
from apis.dataset import dataset
from apis.participant import participant
from apis.study import study
from apis.contributor import contributor
from core import config
from flask import Blueprint, jsonify, request, Response
from flask import Flask
from flask_restx import Api, Resource, reqparse
from model import Study, db, Participant, Dataset, DatasetVersion, DatasetVersions

app = Flask(__name__)
api = Api(
    app,
    title="FAIRHUB",
    description="The backend api system for the Vue app",
    doc="/docs",
)

fhb = api.namespace("fairhub", description="FAIRhub tools")


app.config.from_prefixed_env("FAIRHUB")

if "DATABASE_URL" in app.config:
    print("DATABASE_URL: ", app.config["DATABASE_URL"])
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config["DATABASE_URL"]
else:
    print("FAIRHUB_DATABASE_URL: ", config.FAIRHUB_DATABASE_URL)
    app.config["SQLALCHEMY_DATABASE_URI"] = config.FAIRHUB_DATABASE_URL


model.db.init_app(app)
app.register_blueprint(study)
app.register_blueprint(dataset)
app.register_blueprint(participant)
app.register_blueprint(contributor)


CORS(app)


@app.cli.command("create-schema")
def create_schema():
    model.db.create_all()


@api.route("/")
@api.doc(responses={404: "Todo not found"})
class Home(Resource):
    def home(self):
        return "Home page"


@api.route("/study")
class GetStudy(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def get(self):
        studies = Study.query.all()
        return jsonify([s.to_dict() for s in studies])

    def post(self):
        add_study = Study.from_data(request.json)
        db.session.add(add_study)
        db.session.commit()
        return jsonify(add_study.to_dict())


@api.route("/study/<study_id>")
class UpdateStudy(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def get(self, study_id: int):
        study1 = Study.query.get(study_id)
        return jsonify(study1.to_dict())

    def put(self, study_id: int):
        update_study = Study.query.get(study_id)
        # if not addStudy.validate():
        #     return 'error', 422
        update_study.update(request.json)
        db.session.commit()
        return jsonify(update_study.to_dict())

    def delete(self, study_id: int):
        delete_study = Study.query.get(study_id)
        for d in delete_study.dataset:
            for version in d.dataset_versions:
                version.participants.clear()
        for d in delete_study.dataset:
            for version in d.dataset_versions:
                db.session.delete(version)
            db.session.delete(d)
        for p in delete_study.participants:
            db.session.delete(p)
        db.session.delete(delete_study)
        db.session.commit()
        return "", 204


@api.route("/study/<study_id>/participants")
class AddParticipant(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def get(self, study_id: int):
        participants = Participant.query.all()
        return jsonify([p.to_dict() for p in participants])

    def post(self, study_id: int):
        study = Study.query.get(study_id)
        add_participant = Participant.from_data(request.json, study)
        db.session.add(add_participant)
        db.session.commit()
        return jsonify(add_participant.to_dict()), 201


@api.route("/study/<study_id>/participants/<participant_id>")
class UpdateParticipant(Resource):
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id, participant_id: int):
        update_participant = Participant.query.get(participant_id)
        update_participant.update(request.json)
        db.session.commit()
        return jsonify(update_participant.to_dict())

    def delete(self, study_id, participant_id: int):
        delete_participant = Participant.query.get(participant_id)
        db.session.delete(delete_participant)
        db.session.commit()
        return Response(status=204)


@api.route("/study/<study_id>/dataset")
class AddDataset(Resource):
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def get(self, study_id):
        study = Study.query.get(study_id)
        datasets = Dataset.query.filter_by(study=study)
        return jsonify([d.to_dict() for d in datasets])

    def post(self, study_id):
        study = Study.query.get(study_id)
        dataset_obj = Dataset(study)
        dataset_version = DatasetVersion.from_data(dataset_obj, request.json)
        db.session.add(dataset_obj)
        db.session.add(dataset_version)
        db.session.commit()
        return jsonify(dataset_version.to_dict())


@api.route("/study/<study_id>/dataset/<dataset_id>/version/<version_id>")
class UpdateDataset(Resource):
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def get(study_id, dataset_id, version_id):
        # if int(study_id) not in dic:
        #     return "not found", 404
        dataset_version = DatasetVersion.query.get(version_id)
        return jsonify(dataset_version.to_dict())

    def put(self, study_id, dataset_id, version_id):
        data_version_obj = DatasetVersion.query.get(version_id)
        data_version_obj.update(request.json)
        db.session.commit()
        return jsonify(data_version_obj.to_dict())

    def delete(self, study_id, dataset_id, version_id):
        data_obj = Dataset.query.get(dataset_id)
        for version in data_obj.dataset_versions:
            db.session.delete(version)
            db.session.commit()
        db.session.delete(data_obj)
        db.session.commit()
        return Response(status=204)


@api.route("/study/<study_id>/dataset/<dataset_id>/version")
@api.response(201, "Success")
@api.response(400, "Validation Error")
class PostDataset(Resource):
    def post(study_id, dataset_id):
        data = request.json
        data["participants"] = [Participant.query.get(i) for i in data["participants"]]
        data_obj = Dataset.query.get(dataset_id)
        dataset_version = DatasetVersion.from_data(data, data_obj)
        db.session.add(dataset_version)
        db.session.commit()
        return jsonify(dataset_version.to_dict())


if __name__ == "__main__":
    app.run(debug=True)
