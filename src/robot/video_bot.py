from storage import video_storage, utils, comment_storage
import datetime


def most_popular_job(region: str):
    """[取得當下該國籍所有主題的影片排名及統計資料]

    Args:
        region (str): [國籍]
    """
    category_code = utils.get_db_video_category(regionCode=region)

    # 清單此處增加0是為了取得綜合排行，category:0是總和排行的預設參數
    category_code.append(0)

    if not category_code:
        print("Can't get category code|{}".format(datetime.datetime.now()))
        return False

    for i in category_code:
        res = video_storage.save_most_popular_video(
            regionCode=region, videoCategoryId=int(i))
        print("region:{}|category:{}|{}|UpdateTime:{}".format(
            region, i, res, datetime.datetime.now()))


def upload_video_detail():
    """儲存所有影片的詳情資訊，但已存在的不會更新
    """
    video_list = utils.video_detail_except()
    if not video_list:
        print("Can't get video id|{}".format(datetime.datetime.now()))
        return False

    print("Need update video count:{}".format(len(video_list)))
    for i in video_list:
        if video_storage.save_video_detail(video_id=i):
            print("Update video:{} detail|UpdateTime:{}".format(
                i, datetime.datetime.now()))
        else:
            print("Update video:{} detail error|:{}".format(
                i, datetime.datetime.now()))


def upload_comment(exceptCategory: list, audio_language: str):
    """儲存影片所有留言，已儲存的不會更新
    """
    category_filter = utils.except_specific_category_videoId(
        categoryList=exceptCategory)
    language_filter = utils.specific_default_audio_language_videoId(
        audio_language)
    video_list = list(set(language_filter).intersection(set(category_filter)))
    exist_video_comment = utils.get_db_comment_video_id()
    if not video_list:
        return False

    for i in video_list:
        if i not in exist_video_comment:
            print("Storag videoID:{}".format(i))
            status = comment_storage.save_video_comments(video_id=i)
            print("Update video:{} comment|Status:{}|UpdateTime:{}".format(
                i, status, datetime.datetime.now()))
