from flask import jsonify

from . import blue_channel
from app.storage import channel_storage


@blue_channel.route('/test')
def index():
    return jsonify({"hello": "world"})


@blue_channel.route('/add/<channel>')
def call_channel_storage(channel):
    status = channel_storage.save_channel_subscription(channel_id=channel)
    return jsonify(status)
