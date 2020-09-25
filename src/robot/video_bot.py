from storage import video_storage, utils


def most_popular_job(region: str):
    category_code = utils.get_db_video_category(regionCode=region)
    for i in category_code:
        res = video_storage.save_most_popular_video(
            regionCode=region, videoCategoryId=int(i))
        print("region:{}|category:{}|{}".format(region, i, res))
