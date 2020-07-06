# -*- coding: utf-8 -*-

from oauth.api_oauth import youtube
from utils import error_code


def get_subscriber_by_id(channelId, maxResult=50, pageToken=None):
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

    if not isinstance(subscribers, dict):
        return error_code.SUBSCRIPTIONS_API_ERROR

    return subscribers


if __name__ == "__main__":
    print(get_subscriber_by_id(channelId="UCIF_gt4BfsWyM_2GOcKXyEQ", maxResult=50))
