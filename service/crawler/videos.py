# -*- coding: utf-8 -*-

from oauth.api_oauth import youtube
from utils import error_code


def get_video_detail(videoId: str) -> dict:
    """Video detail

    Args:
        videoId: Youtube videoId

    Returns:
        [dict]:Video detail raw data
        [int]:(3440)VIDEO_DETAIL_ERROR

    """
    try:
        request = youtube.videos().list(
            part="snippet,statistics",
            id=videoId
        )
        response = request.execute()
    except Exception as e:
        response = {"error": e.args[0]["status"]}

    if isinstance(response, dict):
        return response

    return error_code.VIDEO_DETAIL_ERROR
