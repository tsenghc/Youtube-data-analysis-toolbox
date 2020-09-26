from storage import channel_storage, utils


def channel_subscription_crawler():
    channel_list = utils.get_db_channel_list()+utils.channel_list_except()
    for channel in channel_list:
        channel_storage.save_channel_subscription(channel_id=channel)
        print("Save channel {} subscripted".format(channel))


def channel_detail_crawler():
    channel_list = utils.get_db_channel_list()+utils.channel_list_except()
    for channel in channel_list:
        channel_storage.save_channel_detail(channel_id=channel)
        print("Save channel {} detail".format(channel))
