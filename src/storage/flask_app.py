from flask import Flask
from flask_migrate import Migrate

from models.model import db
from utils.config import app_config

migrate = Migrate()

app = Flask(__name__)


def create_app(config_name):
    app.config.from_object(app_config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)

    return app
