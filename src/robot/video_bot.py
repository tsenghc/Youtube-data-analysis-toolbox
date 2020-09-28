from storage import video_storage, utils, comment_storage
import datetime


def most_popular_job(region: str):
    category_code = utils.get_db_video_category(regionCode=region)
    for i in category_code:
        res = video_storage.save_most_popular_video(
            regionCode=region, videoCategoryId=int(i))
        print("region:{}|category:{}|{}|UpdateTime:{}".format(
            region, i, res, datetime.datetime.utcnow()))


def update_video_detail():
    video_list = utils.video_detail_except()
    print(video_list)
    for i in video_list:
        if video_storage.save_video_detail(video_id=i):
            print("Update video:{} detail|UpdateTime:{}".format(
                i, datetime.datetime.utcnow()))


def update_comment():
    video_list = utils.get_db_ChannelPlayListItem_video_id()
    for i in video_list:
        if comment_storage.save_video_comments(video_id=i):
            print("Update video:{} comment|UpdateTime:{}".format(
                i, datetime.datetime.utcnow()))
