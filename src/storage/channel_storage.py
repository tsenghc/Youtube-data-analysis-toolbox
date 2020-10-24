from datetime import datetime
import logging

from crawler import channels, subscriptions
from models.model import (ChannelContentDetail, ChannelList, ChannelSnippet,
                          ChannelStatistics, Subscriptions, db)
from sqlalchemy.exc import SQLAlchemyError
from utils.storage import (channel_list_except, get_db_ChannelList_channel_id,
                           pgsql_0x00_repleace)

from .flask_app import create_app

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
    save_status = {}
    channel_detail = channels.get_channel_detail(channel_id)
    if 'items' not in channel_detail:
        print(channel_detail)
        return False
    channel_detail = channel_detail["items"][0]
    snippet = channel_detail["snippet"]
    statistics = channel_detail["statistics"]
    contentDetails = channel_detail["contentDetails"]
    topicIds = channel_detail.get("topicDetails", {}).get("topicIds", "")
    brandingSettings = channel_detail["brandingSettings"]
    keywords = brandingSettings.get("channel", {}).get("keywords", "")
    channel_list_schemas = {
        "channel_id": channel_id
    }
    # If not get published time,use unix time 0.
    snippet_schemas = {
        "channel_id": channel_id,
        "channel_title": snippet["title"],
        "channel_description": snippet["description"],
        "channel_custom_url": snippet.get("customUrl", ""),
        "channel_published_at": snippet.get("publishedAt", datetime(1970, 1, 1)),
        "channel_thumbnails_url": snippet["thumbnails"]["high"]["url"],
        "channel_country": snippet.get("country", ""),
    }
    statist_schemas = {
        "channel_id": channel_id,
        "view_count": statistics.get("viewCount", 0),
        "comment_count": statistics.get("commentCount", 0),
        "subscriber_count": statistics.get("subscriberCount", 0),
        "video_count": statistics.get("videoCount", 0),
        "hidden_subscriber_count": statistics.get("hiddenSubscriberCount", 0)
    }
    contentDetails_schemas = {
        "channel_id": channel_id,
        "channel_related_playlists": contentDetails["relatedPlaylists"]["uploads"],
        "channel_keywords": topicIds,
        "channel_topic_id": str(keywords).split(" "),
    }
    snippet_model = ChannelSnippet(**pgsql_0x00_repleace(snippet_schemas))
    statist_model = ChannelStatistics(**statist_schemas)
    contentDetails_model = ChannelContentDetail(
        **pgsql_0x00_repleace(contentDetails_schemas))
    channel_list_model = ChannelList(**channel_list_schemas)

    if channel_id not in get_db_ChannelList_channel_id():
        try:
            with app.app_context():
                db.session.add(channel_list_model)
                db.session.commit()
                save_status['channel_list_model'] = True
        except SQLAlchemyError as e:
            save_status['channel_list_model'] = e.args[0]
            # print("channel_list_model_error:{}".format(type(e)))
            pass
    else:
        save_status['channel_list_model'] = "already"

    try:
        with app.app_context():
            db.session.add(snippet_model)
            db.session.commit()
            save_status['snippet_model_error'] = True
    except SQLAlchemyError as e:
        # print("snippet_model_error:{}".format(type(e)))
        save_status['snippet_model_error'] = e.args[0]

    try:
        with app.app_context():
            db.session.add(statist_model)
            db.session.commit()
            save_status['statist_model_error'] = True
    except SQLAlchemyError as e:
        # print("statist_model_error:{}".format(type(e)))
        save_status['statist_model_error'] = e.args[0]
    try:
        with app.app_context():
            db.session.add(contentDetails_model)
            db.session.commit()
            save_status['contentDetails_model_error'] = True
    except SQLAlchemyError as e:
        # print("contentDetails_model_error{}".format(type(e)))
        save_status['contentDetails_model_error'] = e.args[0]

    return save_status


def sync_playlist_with_channelList_channelId() -> bool:
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
                logging.error(
                    "channel_list_model_error:{}".format(type(e.args[0])))
                return False
    return True
