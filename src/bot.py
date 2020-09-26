from apscheduler.schedulers.blocking import BlockingScheduler
from robot import video_bot

scheduler = BlockingScheduler()
scheduler.add_job(video_bot.most_popular_job,
                  'interval', minutes=30, args=("TW",))
scheduler.start()
