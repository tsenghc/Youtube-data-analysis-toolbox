from storage.flask_app import create_app
from models.model import ChannelList, ChannelContentDetail, ChannelStatistics, ChannelSnippet
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import distinct, desc
from utils.database import row2dict
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
