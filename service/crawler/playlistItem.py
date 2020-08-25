# -*- coding: utf-8 -*-

from oauth.api_oauth import youtube
from utils import error_code


def get_playlist_content(playlistId: str, maxResult=50, pageToken=None) -> dict:
    """Get playlist raw data

    Args:
        playlistId:Youtube playlist Id
        maxResult: Result count
        pageToken: Next page token

    Returns:
        [dict]:playlist items raw data
        [int]:(3430)PLAYLIST_ITEMS_ERROR

    """
    try:
        request = youtube.playlistItems().list(
            part="contentDetails",
            maxResults=maxResult,
            pageToken=pageToken,
            playlistId=playlistId
        )
        response = request.execute()
    except Exception as e:
        response = {"error": e.args[0]["status"]}

    if isinstance(response, dict):
        return response

    return error_code.PLAYLIST_ITEMS_ERROR


def get_firstPage_videoId(playlistId: str, maxResult: int) -> list:
    """First page playlist videoId

    Returns:
        [list]:Playlist video list
        [int]:(3430)PLAYLIST_ITEMS_ERROR
    """
    videoId_list = []
    playlist_items = get_playlist_content(playlistId, maxResult)
    if not isinstance(playlist_items, dict):
        return error_code.PLAYLIST_ITEMS_ERROR

    if playlist_items.get("error", False):
        videoId_list.append(playlist_items["error"])
        return videoId_list

    for items in playlist_items["items"]:
        videoId_list.append(items["contentDetails"]["videoId"])
    return videoId_list


def foreach_playlist_videoId(playlistId: str) -> list:
    """Traverse playlist video Id

    Args:
        playlistId: Youtube playlist Id

    Returns:
        [list]:Playlist video list
        [int]:(3430)PLAYLIST_ITEMS_ERROR

    """
    videoId_list = []
    playlist_items = get_playlist_content(playlistId)
    if not isinstance(playlist_items, dict):
        return error_code.PLAYLIST_ITEMS_ERROR

    if playlist_items.get("error", False):
        videoId_list.append(playlist_items["error"])
        return videoId_list

    token = playlist_items.get("nextPageToken", False)

    if not token:
        for items in playlist_items["items"]:
            videoId_list.append(items["contentDetails"]["videoId"])
        return videoId_list

    while token:
        token = playlist_items.get("nextPageToken", False)

        for items in playlist_items["items"]:
            videoId_list.append(items["contentDetails"]["videoId"])
        playlist_items = get_playlist_content(playlistId, pageToken=token)

    if isinstance(videoId_list, list):
        return videoId_list
