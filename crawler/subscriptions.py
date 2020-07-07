# -*- coding: utf-8 -*-

from oauth.api_oauth import youtube
from utils import error_code


def get_subscriber_by_id(channelId: str, maxResult=50, pageToken=None) -> dict:
    """Get a subscriber raw data

    Args:
        channelId ([str]) :Youtube channelId
        maxResult ([int]) :Acceptable values are 0 to 50, inclusive.
                            The default value is 5.

    Returns:
        [dict]:Subscriptions API raw data
        [int]:API error(400)

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
        print(e)

    try:
        if isinstance(subscribers, dict):
            return subscribers
    except Exception as e:
        return error_code.SUBSCRIPTIONS_API_ERROR


def foreach_subscriber_by_channel(channelId: str) -> list[str]:
    """

    Args:
        channelId: Youtube channelId

    Returns:
        [list]:The channel all of subscribers channelId

    """
    subscribers_list = []
    subscribers_data = get_subscriber_by_id(channelId)
    if not isinstance(subscribers_data, dict):
        return error_code.SUBSCRIPTIONS_API_ERROR

    token = subscribers_data.get("nextPageToken", None)

    if not token:
        for items in subscribers_data["items"]:
            subscribers_list.append(items["snippet"]["resourceId"]["channelId"])
        return subscribers_list

    while token is not None:
        try:
            token = subscribers_data["nextPageToken"]
        except Exception as e:
            token = None

        for items in subscribers_data["items"]:
            subscribers_list.append(items["snippet"]["resourceId"]["channelId"])
        subscribers_data = get_subscriber_by_id(channelId, pageToken=token)

    return subscribers_list


if __name__ == "__main__":
    channelId = "UCIF_gt4BfsWyM_2GOcKXyEQ"
    channelId2 = "UC8TtAsZE51ekqffnNASo7DA"
    channelId3 = "UCAfAQOlKYd6ECvqEMiMrjaA"
    print(get_subscriber_by_id(channelId))
    subscriber_list = foreach_subscriber_by_channel(channelId3)
    print((subscriber_list))
