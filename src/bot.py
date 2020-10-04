from apscheduler.schedulers.blocking import BlockingScheduler
from robot import video_bot, channel_bot

if __name__ == '__main__':
    job_defaults = {'max_instances': 2}
    scheduler = BlockingScheduler(job_defaults=job_defaults)

    scheduler.add_job(video_bot.most_popular_job,
                      'cron',
                      minute=30,
                      args=("TW",))

    scheduler.add_job(video_bot.upload_video_detail,
                      'cron',
                      hour=4)

    scheduler.add_job(channel_bot.sync_channelList_channelPlayListItem_channel_id,
                      'cron',
                      hour=6)

    scheduler.add_job(channel_bot.channel_detail_crawler_in_region,
                      'cron',
                      hour=9,
                      args=("TW",))
    scheduler.start()
