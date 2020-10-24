
import logging
from datetime import datetime
from flask_sqlalchemy import utils

from sqlalchemy import util

from crawler import videos
import crawler
from database import db_channel
from robot import channel_bot, video_bot
from storage import (channel_storage, comment_storage, playlist_storage,
                     video_storage)
from utils.storage import channel_list_except, get_db_video_category

FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.DEBUG, filename='main.log',
                    filemode='a', format=FORMAT, datefmt=DATE_FORMAT)

if __name__ == '__main__':
    """Please run setup first

    """
    # video_bot.upload_comment(exceptCategory=[10],audio_language='zh-TW')
    video_bot.most_popular_job("TW")
    # video_bot.upload_video_detail()
    # channel_bot.channel_detail_crawler_in_region("TW")
    # channel_bot.channel_subscription_crawler()
    # channel_bot.sync_channelList_channelPlayListItem_channel_id()
    # channel_bot.unknow_channel_detail_crawler()
    # print(videos.get_video_category("TW"))
    # print(sorted(get_db_video_category("TW")))
