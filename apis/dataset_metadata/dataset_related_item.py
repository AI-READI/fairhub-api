from typing import Any, Union

from flask import request
from flask_restx import Resource, fields

import model
from apis.dataset_metadata_namespace import api

dataset_related_item = api.model(
    "DatasetRelatedItem",
    {
        "id": fields.String(required=True),
        "type": fields.String(required=True),
        "relation_type": fields.String(required=True),
    },
)


@api.route("/study/<study_id>/dataset/<dataset_id>/related-item")
class DatasetRelatedItemResource(Resource):
    @api.doc("related item")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    @api.marshal_with(dataset_related_item)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_related_item_ = dataset_.dataset_related_item
        return [d.to_dict() for d in dataset_related_item_]

    @api.doc("update related item")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        list_of_elements = []
        for i in data:
            if "id" in i and i["id"]:
                dataset_related_item_ = model.DatasetRelatedItem.query.get(i["id"])
                if not dataset_related_item_:
                    return f"{i['id']} Id is not found", 404
                dataset_related_item_.update(i)
                for item in dataset_related_item_.dataset_related_item_title:
                    item.update(i)
                    list_of_elements.append(item.to_dict())
                for item in dataset_related_item_.dataset_related_item_contributor:
                    item.update(i)
                for item in dataset_related_item_.dataset_related_item_identifier:
                    item.update(i)
                for item in dataset_related_item_.dataset_related_item_other:
                    item.update(i)
                list_of_elements.append(dataset_related_item_.to_dict())

            elif "id" not in i or not i["id"]:
                dataset_related_item_ = model.DatasetRelatedItem.from_data(data_obj, i)
                model.db.session.add(dataset_related_item_)

                filtered_related_item = dataset_related_item_.query.filter_by(
                    id=dataset_related_item_.id
                ).first()

                title_add = model.DatasetRelatedItemTitle.from_data(
                    filtered_related_item, i
                )
                model.db.session.add(title_add)

                contributor_add = model.DatasetRelatedItemContributor.from_data(
                    filtered_related_item, i
                )
                model.db.session.add(contributor_add)

                itentifier_add = model.DatasetRelatedItemIdentifier.from_data(
                    filtered_related_item, i
                )
                model.db.session.add(itentifier_add)

                list_of_elements.append(dataset_related_item_.to_dict())

        model.db.session.commit()

        return list_of_elements


@api.route("/study/<study_id>/dataset/<dataset_id>/related-item/<related_item_id>")
class DatasetRelatedItemUpdate(Resource):
    @api.doc("delete related item")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self,
        study_id: int,  # pylint: disable= unused-argument
        dataset_id: int,  # pylint: disable= unused-argument
        related_item_id: int,
    ):
        dataset_related_item_ = model.DatasetRelatedItem.query.get(related_item_id)

        model.db.session.delete(dataset_related_item_)
        model.db.session.commit()

        return 204
