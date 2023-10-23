from typing import Any, Union

from flask import request
from flask_restx import Resource, fields

import model
from apis.authentication import is_granted
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
    # @api.marshal_with(dataset_related_item)
    def get(self, study_id: int, dataset_id: int):  # pylint: disable= unused-argument
        dataset_ = model.Dataset.query.get(dataset_id)
        dataset_related_item_ = dataset_.dataset_related_item
        return [d.to_dict() for d in dataset_related_item_]

    @api.doc("update related item")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def post(self, study_id: int, dataset_id: int):
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return (
                "Access denied, you can not"
                " make any change in dataset metadata"  # noqa: E402
            ), 403
        data: Union[Any, dict] = request.json
        data_obj = model.Dataset.query.get(dataset_id)
        for i in data:
            if "id" in i and i["id"]:
                dataset_related_item_ = model.DatasetRelatedItem.query.get(i["id"])
                if not dataset_related_item_:
                    return f"{i['id']} Id is not found", 404
                dataset_related_item_.update(i)
                # dataset_related_item_.dataset_related_item_other.update(i)

                for title in i["titles"]:
                    if "id" in title and title["id"]:
                        update_title = model.DatasetRelatedItemTitle.query.get(
                            title["id"]
                        )
                        update_title.update(title)
                    else:
                        title_add = model.DatasetRelatedItemTitle.from_data(
                            dataset_related_item_, title
                        )
                        model.db.session.add(title_add)

                for identifier in i["identifiers"]:
                    if "id" in identifier and identifier["id"]:
                        update_identifier = (
                            model.DatasetRelatedItemIdentifier.query.get(
                                identifier["id"]
                            )
                        )
                        update_identifier.update(identifier)
                    else:
                        identifier_add = model.DatasetRelatedItemIdentifier.from_data(
                            dataset_related_item_, identifier
                        )
                        model.db.session.add(identifier_add)
                contributors_ = i["contributors"]
                creators_ = i["creators"]
                for c in contributors_:
                    if "id" in c and c["id"]:
                        related_item_contributors_ = (
                            model.DatasetRelatedItemContributor.query.get(c["id"])
                        )
                        related_item_contributors_.update(c)
                        model.db.session.add(related_item_contributors_)
                    else:
                        related_item_contributors_ = (
                            model.DatasetRelatedItemContributor.from_data(
                                dataset_related_item_, c, False
                            )
                        )
                        model.db.session.add(related_item_contributors_)

                for c in creators_:
                    if "id" in c and c["id"]:
                        related_item_creators_ = (
                            model.DatasetRelatedItemContributor.query.get(c["id"])
                        )

                        related_item_creators_.update(c)
                    else:
                        related_item_creators_ = (
                            model.DatasetRelatedItemContributor.from_data(
                                dataset_related_item_, c, True
                            )
                        )
                        model.db.session.add(related_item_creators_)

                # list_of_elements.append(dataset_related_item_.to_dict())
            elif "id" not in i or not i["id"]:
                dataset_related_item_ = model.DatasetRelatedItem.from_data(data_obj, i)
                model.db.session.add(dataset_related_item_)

                for t in i["titles"]:
                    title_add = model.DatasetRelatedItemTitle.from_data(
                        dataset_related_item_, t
                    )
                    model.db.session.add(title_add)

                for identifier in i["identifiers"]:
                    identifier_add = model.DatasetRelatedItemIdentifier.from_data(
                        dataset_related_item_, identifier
                    )
                    model.db.session.add(identifier_add)

                contributors_ = i["contributors"]
                creators_ = i["creators"]
                for c in contributors_:
                    related_item_contributors_ = (
                        model.DatasetRelatedItemContributor.from_data(
                            dataset_related_item_, c, False
                        )
                    )
                    model.db.session.add(related_item_contributors_)

                for c in creators_:
                    related_item_creators_ = (
                        model.DatasetRelatedItemContributor.from_data(
                            dataset_related_item_, c, True
                        )
                    )
                    model.db.session.add(related_item_creators_)

        model.db.session.commit()
        return [item.to_dict() for item in data_obj.dataset_related_item], 201


@api.route("/study/<study_id>/dataset/<dataset_id>/related-item/<related_item_id>")
class DatasetRelatedItemUpdate(Resource):
    @api.doc("delete related item")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self,
        study_id: int,
        dataset_id: int,  # pylint: disable= unused-argument
        related_item_id: int,
    ):
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        dataset_related_item_ = model.DatasetRelatedItem.query.get(related_item_id)

        model.db.session.delete(dataset_related_item_)
        model.db.session.commit()

        return 204


@api.route(
    "/study/<study_id>/dataset/<dataset_id>/related-item/"
    "<related_item_id>/contributor/<contributor_id>"
)
class RelatedItemContributorsDelete(Resource):
    @api.doc("delete related item contributors")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self,
        study_id: int,
        dataset_id: int,  # pylint: disable= unused-argument
        related_item_id: int,  # pylint: disable= unused-argument
        contributor_id: int,
    ):
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        dataset_contributors_ = model.DatasetRelatedItemContributor.query.get(
            contributor_id
        )
        model.db.session.delete(dataset_contributors_)
        model.db.session.commit()

        return 204


@api.route(
    "/study/<study_id>/dataset/<dataset_id>/"
    "related-item/<related_item_id>/title/<title_id>"
)
class RelatedItemTitlesDelete(Resource):
    @api.doc("delete related item title")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self,
        study_id: int,
        dataset_id: int,  # pylint: disable= unused-argument
        related_item_id: int,  # pylint: disable= unused-argument
        title_id: int,
    ):
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        dataset_title_ = model.DatasetRelatedItemTitle.query.get(title_id)
        model.db.session.delete(dataset_title_)
        model.db.session.commit()
        return 204


@api.route(
    "/study/<study_id>/dataset/<dataset_id>/related-item/"
    "<related_item_id>/identifier/<identifier_id>"
)
class RelatedItemIdentifiersDelete(Resource):
    @api.doc("delete related item identifier")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self,
        study_id: int,
        dataset_id: int,  # pylint: disable= unused-argument
        related_item_id: int,  # pylint: disable= unused-argument
        identifier_id: int,
    ):
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        dataset_identifier_ = model.DatasetRelatedItemIdentifier.query.get(
            identifier_id
        )
        model.db.session.delete(dataset_identifier_)
        model.db.session.commit()
        return 204


@api.route(
    "/study/<study_id>/dataset/<dataset_id>/related-item/"
    "<related_item_id>/creator/<creator_id>"  # pylint: disable = line-too-long
)
class RelatedItemCreatorDelete(Resource):
    @api.doc("delete related item creator")
    @api.response(200, "Success")
    @api.response(400, "Validation Error")
    def delete(
        self,
        study_id: int,
        dataset_id: int,  # pylint: disable= unused-argument
        related_item_id: int,  # pylint: disable= unused-argument
        creator_id: int,
    ):
        study_obj = model.Study.query.get(study_id)
        if not is_granted("dataset_metadata", study_obj):
            return "Access denied, you can not make any change in dataset metadata", 403
        dataset_creator_ = model.DatasetRelatedItemContributor.query.get(creator_id)
        model.db.session.delete(dataset_creator_)
        model.db.session.commit()
        return 204
