# -*- coding: utf-8 -*-

from app.oauth.api_oauth import youtube
from app.utils import error_code


def get_channel_detail(channelId: str) -> dict:
    """Get channel detail

    Args:
        channelId([str]):Youtube channelId

    Returns:
        [dict]:Channels API raw data
        [int]:(3410)CHANNELS_API_ERROR

    """
    try:
        request = youtube.channels().list(
            part="brandingSettings,contentDetails,\
                    localizations,snippet,\
                    statistics,topicDetails",
            id=channelId
        )
        response = request.execute()
    except Exception as e:
        print(e)

    if isinstance(response, dict):
        return response

    return error_code.CHANNELS_API_ERROR
