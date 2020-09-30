from apscheduler.schedulers.blocking import BlockingScheduler
from robot import video_bot, channel_bot

scheduler = BlockingScheduler()

scheduler.add_job(video_bot.most_popular_job,
                  'interval',
                  minutes=30,
                  args=("TW",))

scheduler.add_job(video_bot.upload_video_detail,
                  'interval',
                  hours=12)

scheduler.add_job(channel_bot.sync_channelList_channelPlayListItem_channel_id,
                  'interval',
                  hours=6)

scheduler.add_job(channel_bot.channel_detail_crawler_in_region,
                  'interval',
                  hours=20,
                  args=("TW",))
scheduler.start()
