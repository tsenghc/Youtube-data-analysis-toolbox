from datetime import datetime
from sqlalchemy.sql.functions import user
from .flask_app import create_app
from sqlalchemy.exc import SQLAlchemyError
from .utils import channel_list_except
from crawler import subscriptions, channels
from models.model import Subscriptions, ChannelList, db, ChannelSnippet, ChannelStatistics, \
    ChannelContentDetail

app = create_app('development')


def save_channel_subscription(channel_id: str) -> bool:
    """儲存該頻道公開訂閱使用者訂閱清單及訂閱日期

    Args:
        channel_id: Youtube channel id.

    Returns:
        [bool]:The true if success else fail.

    """
    user_subscribed_day_list = \
        subscriptions.channel_subscriber_day(channel_id)

    if user_subscribed_day_list.get("error"):
        return False
    print("This channel subscribed user have {}".format(
        len(user_subscribed_day_list)))

    for channel in user_subscribed_day_list:
        subscribe_schemas = {
            "resource_channel_id": channel,
            "original_channel_id": channel_id,
            "subscript_at": user_subscribed_day_list[channel],
            "update_time": datetime.utcnow()
        }
        channel_list_schemas = {
            "channel_id": channel
        }
        try:
            with app.app_context():
                db.session.add(ChannelList(**channel_list_schemas))
                db.session.commit()
        except SQLAlchemyError as e:
            print("insert channel_list error:{}".format(type(e)))
        try:
            with app.app_context():
                db.session.add(Subscriptions(**subscribe_schemas))
                db.session.commit()
        except SQLAlchemyError as e:
            print("insert subscripted error:{}".format(type(e)))

    return True


def save_channel_detail(channel_id: str) -> bool:
    """儲存該頻道詳細資訊

    Args:
        channel_id: Youtube channel id.
    Returns:
        [bool]:The true if success else fail.
    """
    channel_detail = channels.get_channel_detail(channel_id)["items"][0]
    snippet = channel_detail["snippet"]
    statistics = channel_detail["statistics"]
    contentDetails = channel_detail["contentDetails"]
    topicIds = channel_detail.get("topicDetails", {}).get("topicIds", "")
    brandingSettings = channel_detail["brandingSettings"]
    keywords = brandingSettings.get("channel", {}).get("keywords", "")
    channel_list_schemas = {
        "channel_id": channel_id
    }
    snippet_schemas = {
        "channel_id": channel_id,
        "channel_title": snippet["title"],
        "channel_description": snippet["description"],
        "channel_custom_url": snippet.get("customUrl", ""),
        "channel_published_at": snippet["publishedAt"],
        "channel_thumbnails_url": snippet["thumbnails"]["high"]["url"],
        "channel_country": snippet.get("country", ""),
    }
    statist_schemas = {
        "channel_id": channel_id,
        "view_count": statistics["viewCount"],
        "comment_count": statistics["commentCount"],
        "subscriber_count": statistics["subscriberCount"],
        "video_count": statistics["videoCount"],
        "hidden_subscriber_count": statistics["hiddenSubscriberCount"],
        "update_time": datetime.utcnow(),
    }
    contentDetails_schemas = {
        "channel_id": channel_id,
        "channel_related_playlists": contentDetails["relatedPlaylists"]["uploads"],
        "channel_keywords": topicIds,
        "channel_topic_id": str(keywords).split(" "),
    }
    snippet_model = ChannelSnippet(**snippet_schemas)
    statist_model = ChannelStatistics(**statist_schemas)
    contentDetails_model = ChannelContentDetail(**contentDetails_schemas)
    channel_list_model = ChannelList(**channel_list_schemas)

    try:
        with app.app_context():
            db.session.add(channel_list_model)
            db.session.commit()
    except SQLAlchemyError as e:
        print("channel_list_model_error:{}".format(type(e)))

    try:
        with app.app_context():
            db.session.add(snippet_model)
            db.session.commit()
    except SQLAlchemyError as e:
        print("snippet_model_error:{}".format(type(e)))

    try:
        with app.app_context():
            db.session.add(statist_model)
            db.session.commit()
    except SQLAlchemyError as e:
        print("statist_model_error:{}".format(type(e)))
    try:
        with app.app_context():
            db.session.add(contentDetails_model)
            db.session.commit()
        return True
    except SQLAlchemyError as e:
        print("contentDetails_model_error{}".format(type(e)))

    return False


def sync_playlist_with_channelList_channelId():
    """同步兩個清單的頻道ID
    """
    channel_list = channel_list_except()
    if channel_list:
        for i in channel_list:
            channel_list_schemas = {
                "channel_id": i
            }
            channel_list_model = ChannelList(**channel_list_schemas)
            try:
                with app.app_context():
                    db.session.add(channel_list_model)
                    db.session.commit()
            except SQLAlchemyError as e:
                print("channel_list_model_error:{}".format(type(e.args[0])))
