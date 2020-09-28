import re
from .flask_app import create_app
from crawler import videos
from models.model import ChannelList, ChannelPlaylistItem, VideoDetail,   db,  VideoCategory
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


def get_db_ChannelList_channel_id():
    try:
        with app.app_context():
            channel_list_id = ChannelList.query.with_entities(
                ChannelList.channel_id).all()
            res = [i for (i,) in channel_list_id]
            return res
    except SQLAlchemyError as e:
        print("get_channel_list:{}".format(type(e)))
    return False


def get_db_ChannelPlayListItem_channel_id():
    try:
        with app.app_context():
            channel_id = ChannelPlaylistItem.query.with_entities(
                distinct(ChannelPlaylistItem.channel_id)).all()
            res = [i for (i,) in channel_id]
            return res
    except SQLAlchemyError as e:
        print("get_playlist_item_id:{}".format(type(e.args[0])))
    return False


def get_db_ChannelPlayListItem_video_id():
    try:
        with app.app_context():
            video_id = ChannelPlaylistItem.query.with_entities(
                distinct(ChannelPlaylistItem.video_id)).all()
            res = [i for (i,) in video_id]
            return res
    except SQLAlchemyError as e:
        print("get_db_ChannelPlayListItem_video_id:{}".format(type(e.args[0])))
    return False


def get_db_VideoDetail_video_id():
    try:
        with app.app_context():
            video_id = VideoDetail.query.with_entities(
                distinct(VideoDetail.video_id)).all()
            res = [i for (i,) in video_id]
            return res
    except SQLAlchemyError as e:
        print("get_db_VideoDetail_video_id:{}".format(type(e.args[0])))
    return False


def channel_list_except():
    channel_list = get_db_ChannelList_channel_id()
    playlist_id = get_db_ChannelPlayListItem_channel_id()
    if channel_list and playlist_id:
        filter_channel = list(set(playlist_id)-set(channel_list))
        return filter_channel
    return False


def video_detail_except():
    playlist_id = get_db_ChannelPlayListItem_video_id()
    video_detial_id = get_db_VideoDetail_video_id()
    if video_detial_id and playlist_id:
        filter_video = set(playlist_id).difference(set(video_detial_id))
        return filter_video
    return False


def vietnamese_repleace(translate_string: str) -> str:
    vietnamese_characters = {
        'a': "áàãạảAÁÀÃẠẢăắằẵặẳĂẮẰẴẶẲâầấẫậẩÂẤẦẪẬẨ",
        'e': "éèẽẹẻEÉÈẼẸẺêếềễệểÊẾỀỄỆỂ",
        'i': "íìĩịỉIÍÌĨỊỈ",
        'o': "óòõọỏOÓÒÕỌỎôốồỗộổÔỐỒỖỘỔơớờỡợởƠỚỜỠỢỞ",
        'u': "úùũụủUÚÙŨỤỦưứừữựửƯỨỪỮỰỬ",
        'y': "ýỳỹỵỷYÝỲỸỴỶ",
        'd': "dđĐD"
    }
    for alpha, vitenames in vietnamese_characters.items():
        for i in vitenames:
            translate_string = translate_string.replace(i, alpha)
    return translate_string
