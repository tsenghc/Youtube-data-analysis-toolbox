from apscheduler.schedulers.blocking import BlockingScheduler
from robot import video_bot, channel_bot

scheduler = BlockingScheduler()

scheduler.add_job(video_bot.most_popular_job,
                  'interval',
                  minutes=30,
                  args=("TW",))

scheduler.add_job(video_bot.upload_video_detail,
                  'interval',
                  minutes=315)

scheduler.add_job(channel_bot.sync_channelList_channelPlayListItem_channel_id,
                  'interval',
                  minutes=50)
scheduler.add_job(channel_bot.channel_detail_crawler, 'interval', minutes=600)
scheduler.start()
