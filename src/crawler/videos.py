# -*- coding: utf-8 -*-
import logging
from sqlalchemy import schema
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
        logging.error(e)
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
            part="snippet,statistics",
            chart="mostPopular",
            maxResults=maxResults,
            pageToken=pageToken,
            regionCode=regionCode,
            videoCategoryId=videoCategoryId
        )
        response = request.execute()
    except Exception as e:
        logging.error(e)
        response = {"error": e.args[0]["status"]}

    if isinstance(response, dict):
        return response


def foreach_most_popular_video(regionCode: str, videoCategoryId: int) -> list:
    """Traverse this category most popular video

    Args:
        regionCode (str): The parameter value is an ISO 3166-1 alpha-2 country code.
        videoCategoryId (int): Youtube categoryId

    Returns:
        list: {id,snippet,statistics}
    """
    video_list = []
    popular_video = get_most_popular_video(regionCode, videoCategoryId)
    if not isinstance(popular_video, dict):
        return error_code.POPULAR_VIDEO_ERROR

    if popular_video.get("error", False):
        video_list.append("error")
        return video_list

    token = popular_video.get("nextPageToken", False)

    if not token:
        for items in popular_video["items"]:
            schema = (items['id'],
                      items['snippet'],
                      items['statistics']
                      )
            video_list.append(schema)
        return video_list

    while token is not False:
        token = popular_video.get("nextPageToken", False)
        for items in popular_video["items"]:
            schema = (items['id'],
                      items['snippet'],
                      items['statistics']
                      )
            video_list.append(schema)
        popular_video = get_most_popular_video(
            regionCode, videoCategoryId, pageToken=token)
    return video_list


def get_video_category(regionCode: str) -> dict:
    """Get video category with region

    Args:
        regionCode (str): The parameter value is an ISO 3166-1 alpha-2 country code.

    Returns:
        [dict]: category detail
    """
    try:
        request = youtube.videoCategories().list(
            part="snippet",
            regionCode=regionCode
        )
        response = request.execute()
    except Exception as e:
        logging.error(e)
        response = {"error": e.args[0]["status"]}
    return response
