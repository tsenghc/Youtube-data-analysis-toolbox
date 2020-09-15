from app.storage import channel_storage, video_storage
from flask import jsonify

from . import blue_channel


@blue_channel.route('/test')
def index():
    return jsonify({"hello": "world"})


@blue_channel.route('/add/<channel>')
def call_channel_storage(channel):
    status = channel_storage.save_channel_subscription(channel_id=channel)
    return jsonify(status)


@blue_channel.route('/popular/<regionCode>/<videoCategoryId>')
def most_popular_video(regionCode, videoCategoryId):
    video = video_storage.save_most_popular_video(regionCode, int(videoCategoryId))
    return jsonify(video)
