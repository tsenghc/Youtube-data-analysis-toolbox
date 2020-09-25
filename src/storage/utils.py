from .flask_app import create_app
from crawler import videos
from models.model import ChannelPlaylistItem, VideoDetail, VideoStatistics, db, MostPopular, VideoCategory
from .playlist_storage import save_channel_playlist_items, save_channel_videoid
from sqlalchemy.exc import SQLAlchemyError
app = create_app('development')


def save_video_categories(regionCode: str):
    category = videos.get_video_category(regionCode=regionCode)
    if not isinstance(category, dict):
        return False
    for i in category['items']:
        schemas = {
            "title": i['snippet']['title'],
            "category_id": i['id'],
            "region_code": regionCode
        }
        category_model = VideoCategory(**schemas)

        try:
            with app.app_context():
                db.session.add(category_model)
                db.session.commit()
        except SQLAlchemyError as e:
            print("video category error:{}".format(type(e)))
            return False

    return True


def get_db_video_category(regionCode: str):
    try:
        with app.app_context():
            code = VideoCategory.query.filter_by(
                region_code=regionCode).with_entities(VideoCategory.category_id).distinct()
            res = [i for (i,) in code]
            return res
    except SQLAlchemyError as e:
        print("check_video_exist:{}".format(type(e)))
    return False
