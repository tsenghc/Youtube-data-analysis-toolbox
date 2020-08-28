# -*- coding: utf-8 -*-

from service.oauth.api_oauth import youtube
from service.utils import error_code


def get_subscriber_by_id(channelId: str,
                         maxResult=50,
                         pageToken=None) -> dict:
    """Get a subscriber raw data

    Args:
        channelId ([str]) :Youtube channelId
        maxResult ([int]) :Acceptable values are 0 to 50, inclusive.
                            The default value is 5.
        pageToken ([None]) : The next page token,usually default None.

    Returns:
        [dict]:Subscriptions API raw data
        [int]:(3400)SUBSCRIPTIONS_API_ERROR

    """
    try:
        request_subscriber = youtube.subscriptions().list(
            part="snippet",
            channelId=channelId,
            maxResults=maxResult,
            pageToken=pageToken
        )
        subscribers = request_subscriber.execute()
    except Exception as e:
        print("channelID:{},Http_code:{}".format(channelId, e.args[0]["status"]))
        subscribers = {"error": e.args[0]["status"]}

    if isinstance(subscribers, dict):
        return subscribers

    return error_code.SUBSCRIPTIONS_API_ERROR


def foreach_subscriber_by_channel(channelId: str) -> list:
    """Traverse subscribers list

    Args:
        channelId: Youtube channelId

    Returns:
        [list]:The channel all of subscribers channelId

    """
    subscribers_list = []
    subscribers_data = get_subscriber_by_id(channelId)
    if not isinstance(subscribers_data, dict):
        return error_code.SUBSCRIPTIONS_API_ERROR

    if subscribers_data.get("error", False):
        subscribers_list.append(subscribers_data["error"])
        return subscribers_list

    token = subscribers_data.get("nextPageToken", False)

    if not token:
        for items in subscribers_data["items"]:
            subscribers_list.append(items["snippet"]["resourceId"]["channelId"])
        return subscribers_list

    while token is not False:
        token = subscribers_data.get("nextPageToken", False)
        for items in subscribers_data["items"]:
            subscribers_list.append(items["snippet"]["resourceId"]["channelId"])
        subscribers_data = get_subscriber_by_id(channelId, pageToken=token)
    return subscribers_list
