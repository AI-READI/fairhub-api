"""API for dataset related identifier"""

from typing import Any, Union

from flask import Response, request
from flask_restx import Resource, fields
from jsonschema import ValidationError, validate

import model
from apis.authentication import is_granted
from apis.dataset_metadata_namespace import api

dataset_related_identifier = api.model(
    "DatasetRelatedIdentifier",
    {
        "id": fields.String(required=True),
        "identifier": fields.String(required=True),
        "identifier_type": fields.String(required=False),
        "relation_type": fields.String(required=False),
        "related_metadata_scheme": fields.String(required=True),
        "scheme_uri": fields.String(required=True),
        "scheme_type": fields.String(required=True),
        "resource_type": fields.String(required=False),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/metadata/related-identifier")
class DatasetRelatedIdentifierResource(Resource):
    """Dataset related identifier Resource"""

    @api.doc("related identifier")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    # @api.marshal_with(dataset_related_identifier)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        """Get dataset related identifier"""
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_related_identifier_ = dataset_.dataset_related_identifier
        return [d.to_dict() for d in dataset_related_identifier_], 200

    @api.doc("update related identifier")
    @api.response(201, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int, dataset_id: int):
        """Update dataset related identifier"""
        study_obj = model.Study.query.get(study_id)

        if not is_granted("dataset_metadata", study_obj):
            return (
                "Access denied, you can not"
                " make any change in dataset metadata"  # noqa: E402
            ), 403

        schema = {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "id": {"type": "string"},
                    "identifier": {"type": "string", "minLength": 1},
                    "identifier_type": {"type": ["string", "null"], "minLength": 1},
                    "relation_type": {"type": ["string", "null"], "minLength": 1},
                    "related_metadata_scheme": {"type": "string"},
                    "scheme_uri": {"type": "string"},
                    "scheme_type": {"type": "string"},
                    "resource_type": {"type": ["string", "null"]},
                },
                "required": [
                    "identifier",
                    "identifier_type",
                    "relation_type",
                    "related_metadata_scheme",
                    "scheme_uri",
                    "scheme_type",
                ],
            },
            "uniqueItems": True,
        }
        try:
            validate(instance=request.json, schema=schema)
        except ValidationError as err:
            return err.message, 400

        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                dataset_related_identifier_ = model.DatasetRelatedIdentifier.query.get(
                    i["id"]
                )
                if not dataset_related_identifier_:
                    return f"{i['id']} Id is not found", 404
                dataset_related_identifier_.update(i)
                list_of_elements.append(dataset_related_identifier_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_related_identifier_ = model.DatasetRelatedIdentifier.from_data(
                    data_obj, i
                )
                model.db.session.add(dataset_related_identifier_)
                list_of_elements.append(dataset_related_identifier_.to_dict())
        model.db.session.commit()
        return list_of_elements, 201


@api.route(
    "/study/<study_id>/dataset/<dataset_id>/metadata/related-identifier/<related_identifier_id>"
)
class DatasetRelatedIdentifierUpdate(Resource):
    """Dataset related identifier Update Resource"""

    @api.doc("delete related identifier")
    @api.response(204, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self,
        study_id: int,
        dataset_id: int,  # pylint: disable= unused-argument
        related_identifier_id: int,
    ):
        """Delete dataset related identifier"""
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        dataset_related_identifier_ = model.DatasetRelatedIdentifier.query.get(
            related_identifier_id
        )

        model.db.session.delete(dataset_related_identifier_)
        model.db.session.commit()

        return Response(status=204)
