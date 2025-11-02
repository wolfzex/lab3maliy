from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py', silent=False)

    db.init_app(app)
    Migrate(app, db)

    # ІМПОРТУЄМО МОДЕЛІ, ЩОБ АЛЕМБІК БАЧИВ ТАБЛИЦІ
    from models.user import UserModel
    from models.category import CategoryModel
    from models.record import RecordModel

    # ПІДКЛЮЧАЄМО РЕСУРСИ (ендпоїнти)
    from resources.user import blp as UserBlueprint
    from resources.category import blp as CategoryBlueprint
    from resources.record import blp as RecordBlueprint

    api = Api(app)
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(CategoryBlueprint)
    api.register_blueprint(RecordBlueprint)

    # БАЗОВІ ХЕНДЛЕРИ ПОМИЛОК (демо)
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
