from .flask_app import create_app
from crawler import videos
from models.model import ChannelList, ChannelPlaylistItem,   db,  VideoCategory
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import distinct

app = create_app('development')


def save_video_categories(regionCode: str):
    category = videos.get_video_category(regionCode=regionCode)
    if not isinstance(category, dict):
        return False
    for i in category['items']:
        schemas = {
            "title": i['snippet']['title'],
            "category_id": i['id'],
            "region_code": regionCode
        }
        category_model = VideoCategory(**schemas)

        try:
            with app.app_context():
                db.session.add(category_model)
                db.session.commit()
        except SQLAlchemyError as e:
            print("video category error:{}".format(type(e)))
            return False

    return True


def get_db_video_category(regionCode: str):
    try:
        with app.app_context():
            code = VideoCategory.query.filter_by(
                region_code=regionCode).with_entities(VideoCategory.category_id).distinct()
            res = [i for (i,) in code]
            return res
    except SQLAlchemyError as e:
        print("check_video_exist:{}".format(type(e)))
    return False


def get_db_channel_list():
    try:
        with app.app_context():
            channel_list_id = ChannelList.query.with_entities(
                ChannelList.channel_id).all()
            res = [i for (i,) in channel_list_id]
            return res
    except SQLAlchemyError as e:
        print("get_channel_list:{}".format(type(e)))
    return False


def get_playlist_item_id():
    try:
        with app.app_context():
            channel_id = ChannelPlaylistItem.query.with_entities(
                distinct(ChannelPlaylistItem.channel_id)).all()
            res = [i for (i,) in channel_id]
            return res
    except SQLAlchemyError as e:
        print("get_playlist_item_id:{}".format(type(e)))
    return False


def channel_list_except():
    channel_list = get_db_channel_list()
    playlist_id = get_playlist_item_id()
    filter_channel = list(set(playlist_id)-set(channel_list))
    return filter_channel
