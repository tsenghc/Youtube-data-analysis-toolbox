# -*- coding: utf-8 -*-

from app.oauth.api_oauth import youtube
from app.utils import error_code


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


def get_most_popular_video(regionCode: str, videoCategoryId: int, maxResults=50, pageToken=None) -> dict:
    """Realtime most popular video

    Args:
        maxResults: API max result
        videoCategoryId:Category id
        regionCode: The parameter value is an ISO 3166-1 alpha-2 country code.

    Returns:
        [dict]:Video detail raw data
    """
    try:
        request = youtube.videos().list(
            part="id",
            chart="mostPopular",
            maxResults=maxResults,
            pageToken=pageToken,
            regionCode=regionCode,
            videoCategoryId=videoCategoryId
        )
        response = request.execute()
    except Exception as e:
        response = {"error": e.args[0]["status"]}

    if isinstance(response, dict):
        return response


def foreach_most_popular_video(regionCode: str, videoCategoryId: int):
    video_list = []
    popular_video = get_most_popular_video(regionCode, videoCategoryId)
    if not isinstance(popular_video, dict):
        return error_code.POPULAR_VIDEO_ERROR

    if popular_video.get("error", False):
        video_list.append(popular_video["error"])
        return video_list

    token = popular_video.get("nextPageToken", False)

    if not token:
        for items in popular_video["items"]:
            video_list.append(items['id'])
        return video_list

    while token is not False:
        token = popular_video.get("nextPageToken", False)
        for items in popular_video["items"]:
            video_list.append(items['id'])
        popular_video = get_most_popular_video(regionCode, videoCategoryId, pageToken=token)
    return video_list
