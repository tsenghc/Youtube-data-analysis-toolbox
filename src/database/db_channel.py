from datetime import datetime
from typing import final

from models.model import (ChannelContentDetail, ChannelList, ChannelSnippet,
                          ChannelStatistics, Subscriptions, db)
from sqlalchemy import desc, distinct
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func
from sqlalchemy.sql.selectable import subquery
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


def get_db_channel_subscribed(channel_id: str):
    """取得該頻道訂閱內容詳細資訊

    Args:
        channel_id (str): [channel_id]

    Returns:
        [list]: [subscribed detail]
    """
    res = []
    try:
        with app.app_context():
            suber = db.session.query(
                Subscriptions.resource_channel_id.label('resource_channel_id'),
                Subscriptions.subscript_at.label('subscript_at')
            ).filter(
                Subscriptions.original_channel_id == channel_id).subquery('suber')

            suber_statist = db.session.query(
                ChannelStatistics.channel_id.label('channel_id'),
                func.max(ChannelStatistics.subscriber_count).label(
                    'subscriber_count'),
                func.max(ChannelStatistics.video_count).label('video_count'),
                func.max(ChannelStatistics.view_count).label('view_count'),
                func.max(ChannelStatistics.comment_count).label(
                    'comment_count'),
                func.max(ChannelStatistics.update_time).label('update_time'),
                suber.c.subscript_at.label('subscript_at')
            ).join(
                ChannelStatistics,
                suber.c.resource_channel_id == ChannelStatistics.channel_id
            ).group_by(
                ChannelStatistics.channel_id, suber.c.subscript_at).subquery()

            query = db.session.query(
                ChannelSnippet.channel_id,
                ChannelSnippet.channel_title,
                ChannelSnippet.channel_country,
                ChannelSnippet.channel_published_at,
                ChannelSnippet.channel_thumbnails_url,
                suber_statist.c.video_count,
                suber_statist.c.subscriber_count,
                suber_statist.c.view_count,
                suber_statist.c.subscript_at,
                func.max(suber_statist.c.update_time).label('update_time')

            ).select_from(
                suber_statist, ChannelSnippet
            ).join(
                ChannelSnippet,
                suber_statist.c.channel_id == ChannelSnippet.channel_id
            ).group_by(
                ChannelSnippet.channel_id,
                ChannelSnippet.channel_title,
                ChannelSnippet.channel_country,
                ChannelSnippet.channel_published_at,
                ChannelSnippet.channel_thumbnails_url,
                suber_statist.c.video_count,
                suber_statist.c.view_count,
                suber_statist.c.subscriber_count,
                suber_statist.c.subscript_at
            ).all()
            if not query:
                return {"result": "notfount"}
    except SQLAlchemyError as e:
        print("get_db_channel_subscribed:{}".format(type(e)))
        return {"error": e.args[0]}

    for i in query:
        sechmes = {
            "channel_id": i[0],
            "channel_title": i[1],
            "channel_country": i[2],
            "channel_published_at": str(i[3]),
            "channel_thumbnails_url": i[4],
            "view_count": i[5],
            "video_count": i[6],
            "subscriber_count": i[7],
            "subscript_at": str(i[8]),
        }
        res.append(sechmes)
    return res
