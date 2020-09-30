
from sqlalchemy import util
from crawler import videos
from storage import video_storage
from robot import channel_bot, video_bot
from storage import utils, comment_storage, playlist_storage
from storage import channel_storage
if __name__ == '__main__':
    """Please run setup first

    """
    # utils.save_video_categories("TW")
    # video_bot.most_popular_job("TW")
    # channel_bot.channel_crawler()
    # channel_bot.channel_detail_crawler()
    # utils.get_db_channel_list()
    # print(len(utils.get_playlist_item_id()))
    # print(len(utils.channel_list_except()))
    # channel_bot.channel_detail_crawler()
    # video_bot.update_video_detail()
    # playlist_storage.save_channel_videoid(
    #     channel_id="UCUGJ-yKqQHl4FSZwUmGpiUg", video_id="pZuFyiuqWik")
    # comment_storage.save_video_comments(video_id="bu8w_g-Cdkg")
    # print(comment_storage.exist_top_comment_id())
    # video_storage.save_video_detail(video_id="-ri7dCN0338")
    # channel_bot.channel_detail_crawler()
    # channel_storage.sync_playlist_with_channelList_channelId()
    # channel_bot.channel_detail_crawler()
    # channel_bot.channel_subscription_crawler()
    # print(len(utils.get_db_region_channel_id("TW")))
    channel_bot.channel_detail_crawler_in_region("TW")
