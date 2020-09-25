# -*- coding: utf-8 -*-
from oauth.api_oauth import youtube
from utils import error_code


def get_channel_playlistId(channelId: str, maxResult=50, pageToken=None) -> dict:
    """

    Args:
        channelId:Youtube channelId
        maxResult:Result count
        pageToken:Next page token

    Returns:
        [dict]:playlist raw data
        [int]:(3420)PLAYLIST_API_ERROR

    """
    try:
        playlist = youtube.playlists().list(
            part="id",
            channelId=channelId,
            maxResults=maxResult,
            pageToken=pageToken
        )
        response = playlist.execute()
    except Exception as e:
        # print("channelID:{},Http_code:{}".format(channelId, e.args[0]["status"]))
        response = {"error": e.args[0]["status"]}

    if isinstance(response, dict):
        return response

    return error_code.PLAYLIST_API_ERROR


def foreach_playlistId_by_channel(channelId: str) -> list:
    """Traverse channel playlistId

    Args:
        channelId:Youtube ChannelId

    Returns:
        [list]:Channel playlistId list
        [int]:(3420)PLAYLIST_API_ERROR

    """
    playlistId_list = []
    playlist_data = get_channel_playlistId(channelId)
    if not isinstance(playlist_data, dict):
        return error_code.PLAYLIST_API_ERROR

    if playlist_data.get("error", False):
        playlistId_list.append(playlist_data["error"])
        return playlistId_list

    token = playlist_data.get("nextPageToken", False)

    if not token:
        for items in playlist_data["items"]:
            playlistId_list.append(items["id"])
        return playlistId_list

    while token:
        token = playlist_data.get("nextPageToken", False)

        for items in playlist_data["items"]:
            playlistId_list.append(items["id"])
        playlist_data = get_channel_playlistId(channelId, pageToken=token)

    if isinstance(playlistId_list, list):
        return playlistId_list
