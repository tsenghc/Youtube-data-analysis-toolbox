import logging

from apscheduler.schedulers.blocking import BlockingScheduler

from robot import channel_bot, video_bot
import datetime
FORMAT = '%(asctime)s %(levelname)s: %(message)s'
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(level=logging.DEBUG, filename='bot-{}.log'.format(datetime.date.today()),
                    filemode='a', format=FORMAT, datefmt=DATE_FORMAT)

if __name__ == '__main__':
    job_defaults = {'max_instances': 2}
    scheduler = BlockingScheduler(job_defaults=job_defaults)
    start = '2020-10-10 09:30:00'
    end = '2030-10-10 09:30:00'
    scheduler.add_job(video_bot.most_popular_job,
                      'cron',
                      minute='0/30',
                      args=("TW",),
                      start_date=start,
                      end_date=end)

    scheduler.add_job(video_bot.upload_video_detail,
                      'cron',
                      hour='*/4',
                      start_date=start,
                      end_date=end)

    scheduler.add_job(channel_bot.sync_channelList_channelPlayListItem_channel_id,
                      'cron',
                      hour='*/6',
                      start_date=start,
                      end_date=end)

    scheduler.add_job(channel_bot.channel_detail_crawler_in_region,
                      'cron',
                      hour='*/9',
                      args=("TW",),
                      start_date=start,
                      end_date=end)
    scheduler.start()
