from storage import video_storage, utils, comment_storage
import datetime


def most_popular_job(region: str):
    """[取得當下該國籍所有主題的影片排名及統計資料]

    Args:
        region (str): [國籍]
    """
    category_code = utils.get_db_video_category(regionCode=region)
    for i in category_code:
        res = video_storage.save_most_popular_video(
            regionCode=region, videoCategoryId=int(i))
        print("region:{}|category:{}|{}|UpdateTime:{}".format(
            region, i, res, datetime.datetime.utcnow()))


def upload_video_detail():
    """儲存所有影片的詳情資訊，但已存在的不會更新
    """
    video_list = utils.video_detail_except()
    print(video_list)
    for i in video_list:
        if video_storage.save_video_detail(video_id=i):
            print("Update video:{} detail|UpdateTime:{}".format(
                i, datetime.datetime.utcnow()))


def upload_comment():
    """儲存影片所有留言，已儲存的不會更新
    """
    video_list = utils.get_db_ChannelPlayListItem_video_id()
    exist_video_comment = utils.get_db_comment_video_id()

    for i in video_list:
        if i not in exist_video_comment:
            print("Storag video:{}...".format(i))
            status = comment_storage.save_video_comments(video_id=i)
            print("Update video:{} comment|Status:{}|UpdateTime:{}".format(
                i, status, datetime.datetime.utcnow()))
