from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import Schema, fields
from flask_jwt_extended import jwt_required

from models import db
from models.record import RecordModel
from models.category import CategoryModel
from models.user import UserModel

blp = Blueprint("Records", "records", description="Expense records")


class RecordSchema(Schema):
    id = fields.Int(dump_only=True)
    amount = fields.Float(required=True)
    description = fields.Str()
    category_id = fields.Int(required=True)
    user_id = fields.Int(required=True)


@blp.route("/record")
class RecordListResource(MethodView):
    @jwt_required()
    @blp.response(200, RecordSchema(many=True))
    def get(self):
        return RecordModel.query.all()

    @jwt_required()
    @blp.arguments(RecordSchema)
    @blp.response(201, RecordSchema)
    def post(self, data):
        if not UserModel.query.get(data["user_id"]):
            abort(400, message="User does not exist.")
        category = CategoryModel.query.get(data["category_id"])
        if not category:
            abort(400, message="Category does not exist.")

        if category.user_id is not None and category.user_id != data["user_id"]:
            abort(403, message="You cannot use someone else's personal category.")

        rec = RecordModel(**data)
        db.session.add(rec)
        db.session.commit()
        return rec


@blp.route("/record/<int:record_id>")
class RecordResource(MethodView):
    @jwt_required()
    @blp.response(200, RecordSchema)
    def get(self, record_id):
        rec = RecordModel.query.get_or_404(record_id)
        return rec

    @jwt_required()
    def delete(self, record_id):
        rec = RecordModel.query.get_or_404(record_id)
        db.session.delete(rec)
        db.session.commit()
        return {"message": "Record deleted."}, 200
