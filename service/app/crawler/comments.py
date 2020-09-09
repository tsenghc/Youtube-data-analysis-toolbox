# -*- coding: utf-8 -*-

from app.oauth.api_oauth import youtube
from app.utils import error_code


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


def foreach_video_comments(videoId: str) -> dict:
    """Traverse comments

    Args:
        videoId: Youtube playlist Id

    Returns:
        [dict]:Video comments
        [int]:(3430)PLAYLIST_ITEMS_ERROR

    """
    top_comments_list = []
    replies_comments_list = []
    comments = {}
    video_comments = get_video_comments(videoId, maxResult=100)
    if not isinstance(video_comments, dict):
        return error_code.VIDEO_COMMENTS_ERROR

    if video_comments.get("error", False):
        return video_comments

    token = video_comments.get("nextPageToken", False)

    if not token:
        for items in video_comments["items"]:
            top_comments_list.append(items["snippet"]["topLevelComment"])
            if "replies" in items:
                replies_comments_list.append(items["replies"]["comments"])
        comments['top_comments_list'] = top_comments_list
        comments['replies_comments_list'] = replies_comments_list
        return comments

    while token:
        token = video_comments.get("nextPageToken", False)
        for items in video_comments["items"]:
            top_comments_list.append(items["snippet"]["topLevelComment"])
            if "replies" in items:
                replies_comments_list.append(items["replies"]["comments"])
        comments['top_comments_list'] = top_comments_list
        comments['replies_comments_list'] = replies_comments_list
        video_comments = get_video_comments(videoId, maxResult=100, pageToken=token)

    if isinstance(top_comments_list, list):
        return comments
