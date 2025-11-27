from flask_smorest import Blueprint, abort
from flask.views import MethodView
from marshmallow import Schema, fields
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, jwt_required

from models import db
from models.user import UserModel

blp = Blueprint("Users", "users", description="Operations on users")


class UserRegisterSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)


class UserLoginSchema(Schema):
    username = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    @blp.response(201, UserSchema)
    def post(self, data):
        if UserModel.query.filter_by(username=data["username"]).first():
            abort(409, message="User with this username already exists.")

        hashed = pbkdf2_sha256.hash(data["password"])
        user = UserModel(username=data["username"], password=hashed)
        db.session.add(user)
        db.session.commit()
        return user


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserLoginSchema)
    def post(self, data):
        user = UserModel.query.filter_by(username=data["username"]).first()
        if not user or not pbkdf2_sha256.verify(data["password"], user.password):
            abort(401, message="Invalid credentials.")

        token = create_access_token(identity=str(user.id))
        return {"access_token": token, "user_id": user.id}, 200


@blp.route("/user")
class UsersListResource(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()


@blp.route("/user/<int:user_id>")
class UserResource(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    @jwt_required()
    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
