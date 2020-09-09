from flask import Blueprint

blue_channel = Blueprint('channel', __name__)

from . import channel
