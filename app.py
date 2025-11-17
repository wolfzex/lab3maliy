import os
from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from models import db

from models.user import UserModel
from models.category import CategoryModel
from models.record import RecordModel

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py', silent=False)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    db.init_app(app)
    Migrate(app, db)
    
    jwt = JWTManager(app)

    from resources.user import blp as UserBlueprint
    from resources.category import blp as CategoryBlueprint
    from resources.record import blp as RecordBlueprint

    api = Api(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(RecordBlueprint)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )
    
    @app.errorhandler(404)
    def not_found(e):
        return jsonify(message="Not found"), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify(message="Internal server error"), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)