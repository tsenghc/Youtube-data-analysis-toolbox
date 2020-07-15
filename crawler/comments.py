# -*- coding: utf-8 -*-

from oauth.api_oauth import youtube
from utils import error_code


def get_video_comments(videoId: str, maxResult: int, pageToken=None, order="time") -> dict:
    """Video comments raw data

    Args:
        videoId: Youtube videoId
        maxResult: Acceptable values are 1 to 100, inclusive. The default value is 20.
        pageToken: Next page token
        order:
            time - Comment threads are ordered by time. This is the default behavior.
            relevance - Comment threads are ordered by relevance.

    Returns:
        [dict]:Comments raw data
        [int]:(3450)VIDEO_COMMENTS_ERROR

    """
    try:
        request = youtube.commentThreads().list(
            part="snippet,replies",
            maxResults=maxResult,
            moderationStatus="published",
            order=order,
            pageToken=pageToken,
            videoId=videoId
        )
        response = request.execute()
    except Exception as e:
        response = {"error": e.args[0]["status"]}

    if isinstance(response, dict):
        return response

    return error_code.VIDEO_COMMENTS_ERROR
