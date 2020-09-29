from storage import channel_storage, utils


def channel_subscription_crawler():
    """儲存該頻道訂閱的內容
    """
    channel_list = utils.get_db_ChannelList_channel_id()+utils.channel_list_except()
    for channel in channel_list:
        channel_storage.save_channel_subscription(channel_id=channel)
        print("Save channel {} subscripted".format(channel))


def channel_detail_crawler():
    """儲存channelList中的頻道資訊
    """
    channel_list = utils.get_db_ChannelList_channel_id()
    for channel in channel_list:
        channel_storage.save_channel_detail(channel_id=channel)
        print("Save channel {} detail".format(channel))


def sync_channelList_channelPlayListItem_channel_id():
    """同步channelList與channelPlaylistItem兩表的channelId
    """
    channel_storage.sync_playlist_with_channelList_channelId()
