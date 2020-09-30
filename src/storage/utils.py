import re
from .flask_app import create_app
from crawler import videos
from models.model import ChannelList, ChannelPlaylistItem, ChannelSnippet, TopLevelComment, VideoDetail,   db,  VideoCategory
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import distinct

app = create_app('development')


def save_video_categories(regionCode: str):
    """儲存該國籍的主題內容

    Args:
        regionCode (str): 國籍簡碼

    Returns:
        [bool]: 成功或報錯
    """
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
    """取得該國即目前已有的主題代號

    Args:
        regionCode (str): [國籍簡碼]

    Returns:
        [list]: [可用的主題代號]
    """
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
    """取得資料庫Table:channellist表中的channel_id

    Returns:
        [list]: [channel list]
    """
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
    """取得在Table:channelPlaylistItem中的channel_id

    Returns:
        [list]: [channel list]
    """
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
    """取得在Table:channelPlaylistItem中的video_id

    Returns:
        [list]: [video_id list]
    """
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
    """取得Table:videoDetail中的video_id

    Returns:
        [list]: [video id list]
    """
    try:
        with app.app_context():
            video_id = VideoDetail.query.with_entities(
                distinct(VideoDetail.video_id)).all()
            res = [i for (i,) in video_id]
            return res
    except SQLAlchemyError as e:
        print("get_db_VideoDetail_video_id:{}".format(type(e.args[0])))
    return False


def get_db_comment_video_id():
    """取得Table:topLevelComment中的video_id

    Returns:
        [list]: [video id list]
    """
    try:
        with app.app_context():
            video_id = TopLevelComment.query.with_entities(
                distinct(TopLevelComment.video_id)).all()
            res = [i for (i,) in video_id]
            return res
    except SQLAlchemyError as e:
        print("get_db_comment_video_id:{}".format(type(e.args[0])))
    return False


def get_db_region_channel_id(region_code: str):
    try:
        with app.app_context():
            channel_id = db.session.query(distinct(ChannelSnippet.channel_id)).join(
                ChannelPlaylistItem,
                ChannelSnippet.channel_id == ChannelPlaylistItem.channel_id).filter(
                    ChannelSnippet.channel_country == region_code)
            res = [i for (i,) in channel_id]
            return res
    except SQLAlchemyError as e:
        print("get_db_region_channel_id:{}".format(type(e.args[0])))
    return False


def channel_list_except():
    """取得channelList/channelPlayListItem兩表的channel_id差集

    Returns:
        [list]]: [目前尚未同步過去channel_list的channel_id]
    """
    channel_list = get_db_ChannelList_channel_id()
    playlist_id = get_db_ChannelPlayListItem_channel_id()
    if channel_list or playlist_id:
        filter_channel = list(set(playlist_id)-set(channel_list))
        return filter_channel
    return False


def video_detail_except():
    """取得channelPlayListItem/videoDetail兩表video_id的差集

    Returns:
        [list]: [目前尚未儲存詳細資料的影片ID]
    """
    playlist_id = get_db_ChannelPlayListItem_video_id()
    video_detail_id = get_db_VideoDetail_video_id()
    if video_detail_id and playlist_id:
        filter_video = list(set(playlist_id).difference(set(video_detail_id)))
        return filter_video
    return False


def vietnamese_repleace(translate_string: str):
    """越南音標文轉換英文字母

    Args:
        translate_string (str): [待轉換的字串]

    Returns:
        str: [轉換完畢的字串]
    """
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


def pgsql_0x00_repleace(reatranslate_string: str):
    """NULL空字元轉換

    Args:
        reatranslate_string (str): [待轉換的字串]

    Returns:
        str: [轉換完畢的字串]
    """
    for k, v in reatranslate_string.items():
        reatranslate_string[k] = str(v).replace('\x00', "")
    return reatranslate_string
