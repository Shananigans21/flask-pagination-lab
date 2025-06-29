from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from sqlalchemy import MetaData

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)
migrate = Migrate()
api = Api()

def create_app(env="dev"):
    app = Flask(__name__)
    if env == "test":
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:",
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
            TESTING = True,
            JSON_SORT_KEYS = False
        )
    else:
        app.config.from_mapping(
            SQLALCHEMY_DATABASE_URI = "sqlite:///app.db",
            SQLALCHEMY_TRACK_MODIFICATIONS = False,
            JSON_SORT_KEYS = False,
            DEBUG = True
        )
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    return app
