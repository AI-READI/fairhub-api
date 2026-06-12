"""API for dataset title metadata"""

from typing import Any, Union

from flask import Response, request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api

dataset_general_information = api.model(
    "DatasetGeneralInformation",
    {
        "titles": fields.List(
            fields.Nested(
                api.model(
                    "DatasetTitle",
                    {
                        "id": fields.String(required=True),
                        "title": fields.String(required=True),
                        "type": fields.String(required=True),
                    },
                )
            )
        ),
        "descriptions": fields.List(
            fields.Nested(
                api.model(
                    "DatasetDescription",
                    {
                        "id": fields.String(required=True),
                        "description": fields.String(required=True),
                        "type": fields.String(required=True),
                    },
                )
            )
        ),
        "dates": fields.List(
            fields.Nested(
                api.model(
                    "DatasetDate",
                    {
                        "id": fields.String(required=True),
                        "date": fields.Integer(required=True),
                        "type": fields.String(required=True),
                        "information": fields.String(required=True),
                    },
                )
            )
        ),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/general-information")
class DatasetGeneralInformation(Resource):
    """Dataset General Information Resource"""

    @api.doc("title")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.param("id", "The dataset identifier")
    @api.marshal_with(dataset_general_information)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset title"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_title_ = dataset_.dataset_title
        dataset_description_ = dataset_.dataset_description
        dataset_date_ = dataset_.dataset_date
        return {
            "titles": [d.to_dict() for d in dataset_title_],
            "descriptions": [d.to_dict() for d in dataset_description_],
            "dates": [d.to_dict() for d in dataset_date_],
        }, 200

    @api.doc("update general information")
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_general_information)
    def post(self, study_id: int, dataset_id: int):
        """Update dataset title"""
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        schema = {
            "type": "object",
            "additionalProperties": False,
            "properties": {
                "titles": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "title": {"type": "string", "minLength": 1},
                            "type": {
                                "type": "string",
                                "enum": [
                                    "MainTitle",
                                    "AlternativeTitle",
                                    "Subtitle",
                                    "TranslatedTitle",
                                    "OtherTitle",
                                ],
                            },
                        },
                        "required": ["title", "type"],
                    },
                },
                "descriptions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "description": {"type": "string", "minLength": 1},
                            "type": {
                                "type": "string",
                                "enum": [
                                    "Abstract",
                                    "Methods",
                                    "SeriesInformation",
                                    "TableOfContents",
                                    "TechnicalInfo",
                                    "Other",
                                ],
                            },
                        },
                        "required": ["description", "type"],
                    },
                },
                "dates": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "date": {"type": "integer"},
                            "type": {"type": "string", "minLength": 1},
                            "information": {"type": "string"},
                        },
                        "required": ["date", "type", "information"],
                    },
                },
            },
        }
        try:
            validate(request.json, schema)
        except ValidationError as e:
            return e.message, 400

        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        list_of_titles = []
        for i in data["titles"]:
            if "id" in i and i["id"]:
                dataset_title_ = model.DatasetTitle.query.get(i["id"])
                dataset_title_.update(i)
                list_of_titles.append(dataset_title_.to_dict())
            elif "id" not in i or not i["id"]:
                if i["type"] == "MainTitle":
                    return (
                        "Main Title type can not be given",
                        403,
                    )
                dataset_title_ = model.DatasetTitle.from_data(data_obj, i)
                model.db.session.add(dataset_title_)
                list_of_titles.append(dataset_title_.to_dict())

        list_of_description = []
        for i in data["descriptions"]:
            if "id" in i and i["id"]:
                dataset_description_ = model.DatasetDescription.query.get(i["id"])
                # if dataset_description_.type == "Abstract":
                #     return (
                #         "Abstract type can not be modified",
                #         403,
                #     )
                dataset_description_.update(i)
                list_of_description.append(dataset_description_.to_dict())
            elif "id" not in i or not i["id"]:
                if i["type"] == "Abstract":
                    return (
                        "Abstract type in description can not be given",
                        403,
                    )
                dataset_description_ = model.DatasetDescription.from_data(data_obj, i)
                model.db.session.add(dataset_description_)
                list_of_description.append(dataset_description_.to_dict())

        list_of_dates = []
        for i in data["dates"]:
            if "id" in i and i["id"]:
                dataset_date_ = model.DatasetDate.query.get(i["id"])
                if not dataset_date_:
                    return f"Study link {i['id']} Id is not found", 404
                dataset_date_.update(i)
                list_of_dates.append(dataset_date_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_date_ = model.DatasetDate.from_data(data_obj, i)
                model.db.session.add(dataset_date_)
                list_of_dates.append(dataset_date_.to_dict())

        model.db.session.commit()

        return (
            {
                "titles": list_of_titles,
                "descriptions": list_of_description,
                "dates": list_of_dates,
            },
            200,
        )


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/title/<title_id>")
class DatasetTitleDelete(Resource):
    """Dataset Title Update Resource"""

    @api.doc("delete title")
    @api.response(204, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self,
        study_id: int,
        dataset_id: int,  # pylint: disable= unused-argument
        title_id: int,
    ):
        """Delete dataset title"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return (
                "Access denied, you can not make any change in dataset metadata",
                403,
            )
        dataset_title_ = model.DatasetTitle.query.get(title_id)
        if dataset_title_.type == "MainTitle":
            return (
                "Main Title type can not be deleted",
                403,
            )
        model.db.session.delete(dataset_title_)
        model.db.session.commit()
        return Response(status=204)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/date/<date_id>")
class DatasetDateDeleteResource(Resource):
    """Dataset Date Delete Resource"""

    @api.doc("delete date")
    @api.response(204, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self, study_id: int, dataset_id: int, date_id: int
    ):  # pylint: disable= unused-argument
        """Delete dataset date"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        date_ = model.DatasetDate.query.get(date_id)

        model.db.session.delete(date_)
        model.db.session.commit()
        return Response(status=204)

    @api.route(
        "/study/<study_id>/dataset/<dataset_id>/"
        "metadata/description/<description_id>"
    )
    class DatasetDescriptionUpdate(Resource):
        """Dataset Description Update Resource"""

        @api.doc("delete description")
        @api.response(204, "Success")
        @api.response(400, "Validation Error")
        def delete(
            self,
            study_id: int,
            dataset_id: int,  # pylint: disable= unused-argument
            description_id: int,
        ):
            """Delete dataset description"""
            study_obj = model.Study.query.get(study_id)
            if not is_granted("dataset_metadata", study_obj):
                return (
                    "Access denied, you can not make any change in dataset metadata",
                    403,
                )
            dataset_description_ = model.DatasetDescription.query.get(description_id)
            if dataset_description_.type == "Abstract":
                return (
                    "Abstract description can not be deleted",
                    403,
                )
            model.db.session.delete(dataset_description_)
            model.db.session.commit()

            return Response(status=204)
