from collections import Counter
from flask_restful import Resource
from flask import request
from models.item import ItemModel
import stripe

from models.order import OrderModel, ItemsInOrder
from libs.strings import gettext

from schemas.order import OrderSchema

order_schema = OrderSchema()


class Order(Resource):
    @classmethod
    def get(cls):
        return order_schema.dump(OrderModel.find_all(), many=True), 200

    @classmethod
    def post(cls):
        data = request.get_json()
        items = []
        item_id_quantities = Counter(data["item_ids"])

        for _id, count in item_id_quantities.most_common():
            item = ItemModel.find_by_id(_id)
            if not item:
                return {"message": gettext("item_by_id_not_found").format(_id)}, 404

            items.append(ItemsInOrder(item_id=_id, quantity=count))

        order = OrderModel(items=items, status="pending")
        order.save_to_db()

        order.set_status("failed")

        try:
            order.charge_with_stripe(data["token"])
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            return e.code, e.http_status
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            return e.code, e.http_status
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            return e.code, e.http_status
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            return e.code, e.http_status
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            return e.code, e.http_status
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            return e.code, e.http_status
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            return {"message": gettext("order_error")}, 500

        order.set_status("complete")
        return order_schema.dump(order)
