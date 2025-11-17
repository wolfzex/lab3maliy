from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import Schema, fields
from flask_jwt_extended import jwt_required

from models import db
from models.category import CategoryModel
from models.user import UserModel

blp = Blueprint("Categories", "categories", description="Expense categories")

class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    is_global = fields.Bool(load_default=False)
    user_id = fields.Int(allow_none=True)

@blp.route("/category")
class CategoryList(MethodView):
    @jwt_required()
    @blp.response(200, CategorySchema(many=True))
    def get(self):
        return CategoryModel.query.all()

    @jwt_required()
    @blp.arguments(CategorySchema)
    @blp.response(201, CategorySchema)
    def post(self, data):
        if data.get("is_global"):
            data["user_id"] = None
        else:
            uid = data.get("user_id")
            if uid is None or not UserModel.query.get(uid):
                abort(400, message="Personal category requires valid user_id.")
        cat = CategoryModel(**data)
        db.session.add(cat)
        db.session.commit()
        return cat