from flask import Flask
from flask_migrate import Migrate
from .models import db

from .config.config import config

migrate = Migrate()

app = Flask(__name__)

def create_app(config_name):
    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)

    from .views import blue_channel
    app.register_blueprint(blue_channel, url_prefix='/channel')

    return app
