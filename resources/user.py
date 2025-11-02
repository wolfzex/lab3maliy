from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import Schema, fields
from models import db
from models.user import UserModel

blp = Blueprint("Users", "users", description="Operations on users")

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)

@blp.route("/user")
class UserList(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    @blp.arguments(UserSchema)
    @blp.response(201, UserSchema)
    def post(self, data):
        if UserModel.query.filter_by(username=data["username"]).first():
            abort(400, message="User already exists.")
        user = UserModel(**data)
        db.session.add(user)
        db.session.commit()
        return user
