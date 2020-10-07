from models.model import (ChannelContentDetail, ChannelList, ChannelSnippet,
                          ChannelStatistics)
from sqlalchemy import desc, distinct
from sqlalchemy.exc import SQLAlchemyError
from storage.flask_app import create_app
from utils.database import row2dict, tuple2list

app = create_app('development')


def get_db_channel_detail(channel_id: str) -> dict:
    try:
        with app.app_context():
            query = ChannelSnippet.query.filter(
                ChannelSnippet.channel_id == channel_id).order_by(desc('update_time')).first()
            if isinstance(query, ChannelSnippet):
                channel_detail = row2dict(query)
                return channel_detail
            return {"error": "not found"}
    except SQLAlchemyError as e:
        print("get_db_channel_detail:{}".format(type(e)))
    return {"error": "query error"}


def get_db_unknow_channel_id() -> list:
    """取得尚未儲存頻道詳細資訊的頻道ID

    Returns:
        [list]: [channel_id]
    """
    try:
        with app.app_context():
            exist_detail = ChannelSnippet.query.with_entities(
                ChannelSnippet.channel_id).group_by(ChannelSnippet.channel_id).all()
            channel_detail = tuple2list(exist_detail)

            query = ChannelList.query.with_entities(
                ChannelList.channel_id).filter(
                ChannelList.channel_id.notin_(channel_detail)).all()
            res = tuple2list(query)
            return res
    except SQLAlchemyError as e:
        print("get_db_channel_detail:{}".format(type(e)))
    return {"error": "query error"}
