from flask_restful import Resource
from flask import request
from models.item import ItemModel

from models.order import OrderModel
from libs.strings import gettext


class Order(Resource):
    @classmethod
    def post(cls):
        data = request.get_json()
        items = []

        for _id in data["item_ids"]:
            item = ItemModel.find_by_id(_id)
            if not item:
                return {"message": gettext("item_by_id_not_found").format(_id)}, 404

            items.append(item)

        order = OrderModel(items=items, status="pending")
        order.save_to_db()

        order.set_status("something")
