import os
from typing import List
from db import db


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(20), nullable=False)

    items = db.relationship("ItemModel", lazy="dynamic")

    # order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    # order = db.relationship("OrderModel")
    @classmethod
    def find_by_id(cls, _id: int) -> "OrderModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["OrderModel"]:
        return cls.query.all()

    def set_status(self, new_status: str) -> None:
        self.status = new_status
        db.save_to_db()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
