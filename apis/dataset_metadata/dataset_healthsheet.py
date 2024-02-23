"""API endpoints for dataset healthsheet"""

from flask import request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api

#
dataset_health_sheet_motivation = api.model(
    "DatasetHealthSheetMotivation",
    {
        "motivation": fields.String(required=True),
    },
)
dataset_health_sheet_composition = api.model(
    "DatasetHealthSheetComposition",
    {
        "composition": fields.String(required=True),
    },
)
dataset_health_sheet_collection = api.model(
    "DatasetHealthSheetCollection",
    {
        "collection": fields.String(required=True),
    },
)
dataset_health_sheet_preprocessing = api.model(
    "DatasetHealthSheetPreprocessing",
    {
        "preprocessing": fields.String(required=True),
    },
)
dataset_health_sheet_uses = api.model(
    "DatasetHealthSheetUses",
    {
        "uses": fields.String(required=True),
    },
)
dataset_health_sheet_distribution = api.model(
    "DatasetHealthSheetDistribution",
    {
        "distribution": fields.String(required=True),
    },
)
dataset_health_sheet_maintenance = api.model(
    "DatasetHealthSheetMaintenance",
    {
        "maintenance": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/healthsheet/motivation")
class DatasetHealthsheetMotivation(Resource):
    """Dataset health sheet motivation"""

    @api.doc("health sheet motivation")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_health_sheet_motivation)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset health sheet motivation"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_health_sheet_ = dataset_.dataset_healthsheet

        return {"motivation": dataset_health_sheet_.motivation}, 200

    @api.doc("health sheet motivation")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):
        """Update dataset health sheet motivation"""
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "motivation": {"type": "string"},
            },
            "required": [
                "motivation",
            ],
        }
        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_healthsheet.update(data)
        model.db.session.commit()
        return {"motivation": dataset_.dataset_healthsheet.motivation}, 200


@api.route("/study/<study_id>/dataset/<dataset_id>/healthsheet/maintenance")
class DatasetHealthSheetMaintenance(Resource):
    """Dataset health sheet maintenance"""

    @api.doc("health sheet maintenance")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_health_sheet_maintenance)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset healthsheet maintenance"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_health_sheet_ = dataset_.dataset_healthsheet

        return {"maintenance": dataset_health_sheet_.maintenance}, 200

    @api.doc("healthSheet maintenance")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):
        """Update dataset health sheet maintenance"""
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "maintenance": {"type": "string"},
            },
            "required": [
                "maintenance",
            ],
        }
        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_healthsheet.update(data)
        model.db.session.commit()
        return {"maintenance": dataset_.dataset_healthsheet.maintenance}, 200


@api.route("/study/<study_id>/dataset/<dataset_id>/healthsheet/composition")
class DatasetHealthSheetComposition(Resource):
    """Dataset healthsheet composition"""

    @api.doc("health sheet composition")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_health_sheet_composition)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset health sheet composition"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_health_sheet_ = dataset_.dataset_healthsheet

        return {"composition": dataset_health_sheet_.composition}, 200

    @api.doc("health sheet composition")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):
        """Update dataset health sheet composition"""
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "composition": {"type": "string"},
            },
            "required": [
                "composition",
            ],
        }
        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_healthsheet.update(data)
        model.db.session.commit()
        return {"composition": dataset_.dataset_healthsheet.composition}, 200


@api.route("/study/<study_id>/dataset/<dataset_id>/healthsheet/collection")
class DatasetHealthSheetCollection(Resource):
    """Dataset health sheet Resource"""

    @api.doc("health sheet collection")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_health_sheet_collection)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset health sheet collection"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_health_sheet_ = dataset_.dataset_healthsheet

        return {"collection": dataset_health_sheet_.collection}, 200

    @api.doc("healthsheet collection")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):
        """Update dataset health sheet collection"""
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "collection": {"type": "string"},
            },
            "required": [
                "collection",
            ],
        }
        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_healthsheet.update(data)
        model.db.session.commit()
        return {"collection": dataset_.dataset_healthsheet.collection}, 200


@api.route("/study/<study_id>/dataset/<dataset_id>/healthsheet/preprocessing")
class DatasetHealthSheetPreprocessing(Resource):
    """Dataset health sheet preprocessing"""

    @api.doc("health sheet preprocessing")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_health_sheet_preprocessing)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset health sheet collection"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_health_sheet_ = dataset_.dataset_healthsheet

        return {"preprocessing": dataset_health_sheet_.preprocessing}, 200

    @api.doc("healthsheet preprocessing")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):
        """Update dataset healthsheet preprocessing"""
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "preprocessing": {"type": "string"},
            },
            "required": [
                "preprocessing",
            ],
        }
        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_healthsheet.update(data)
        model.db.session.commit()
        return {"collection": dataset_.dataset_healthsheet.collection}, 200


@api.route("/study/<study_id>/dataset/<dataset_id>/healthsheet/uses")
class DatasetHealthSheetUses(Resource):
    """Dataset healthsheet uses Resource"""

    @api.doc("health sheet uses")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_health_sheet_uses)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset health sheet collection"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_health_sheet_ = dataset_.dataset_healthsheet

        return {"uses": dataset_health_sheet_.uses}, 200

    @api.doc("health sheet uses")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):
        """Update dataset health sheet uses"""
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "uses": {"type": "string"},
            },
            "required": [
                "uses",
            ],
        }
        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_healthsheet.update(data)
        model.db.session.commit()
        return {"uses": dataset_.dataset_healthsheet.uses}, 200


@api.route("/study/<study_id>/dataset/<dataset_id>/healthsheet/distribution")
class DatasetHealthSheetDistribution(Resource):
    """Dataset health sheet distribution Resource"""

    @api.doc("health sheet distribution distribution")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_health_sheet_distribution)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset health sheet collection"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_health_sheet_ = dataset_.dataset_healthsheet

        return {"distribution": dataset_health_sheet_.distribution}, 200

    @api.doc("healthsheet distribution")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def put(self, study_id: int, dataset_id: int):
        """Update dataset health sheet uses"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403

        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "distribution": {"type": "string"},
            },
            "required": [
                "distribution",
            ],
        }
        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data = request.json
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_.dataset_healthsheet.update(data)
        model.db.session.commit()
        return {"distribution": dataset_.dataset_healthsheet.distribution}, 200
