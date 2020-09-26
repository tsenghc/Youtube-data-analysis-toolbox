import re
from .flask_app import create_app
from crawler import videos
from models.model import ChannelPlaylistItem, VideoDetail, VideoStatistics, db, MostPopular
from .playlist_storage import save_channel_playlist_items, save_channel_videoid
from sqlalchemy.exc import SQLAlchemyError
app = create_app('development')


def check_video_exist(video_id: str) -> bool:
    """確認該影片是否存在於PlaylistItem欄位中

    Returns:
        [bool]:
    """
    try:
        with app.app_context():
            video = ChannelPlaylistItem.query.filter_by(
                video_id=video_id).first()
            if video is not None:
                return True
    except SQLAlchemyError as e:
        print("check_video_exist:{}".format(type(e)))
    return False


def get_channel_video_list(channel_id: str) -> list:
    """取得ChannelPlaylistItem表中的影片清單

    Returns:
        [list]:Channel video ID
    """
    video_list = []
    try:
        with app.app_context():
            query = ChannelPlaylistItem.query.filter_by(
                channel_id=channel_id).all()
            if not query:
                save_channel_playlist_items(channel_id)
                get_channel_video_list(channel_id)
            else:
                video_list = [i.video_id for i in query]
            return video_list
    except SQLAlchemyError as e:
        print(type(e))
    return video_list


def save_channel_video_detail(channel_id: str) -> bool:
    """儲存該頻道所有影片詳細資訊及統計資料
    先取得DB中的影片清單，並將影片資訊逐一遍歷，並儲存至DB中

    Returns:
        [bool]:
    """
    snippet_ORM = []
    statistics_ORM = []
    progress = 0
    video_list = get_channel_video_list(channel_id)
    print("This channel have {} video".format(len(video_list)))
    if not video_list:
        return False

    for video_id in video_list:
        detail = videos.get_video_detail(video_id)
        if 'items' not in detail:
            continue
        detail = detail['items'][0]
        snippet_schemas = {
            "video_id": video_id,
            "title": detail['snippet']['title'],
            "description": detail['snippet']['description'],
            "video_published_at": detail['snippet']['publishedAt'],
            "tags": detail['snippet'].get('tags', []),
            "category_id": detail['snippet']['categoryId'],
            "default_audio_language": detail.get('snippet', {}).get('defaultAudioLanguage', 'none'),
            "live_broadcast_content": detail['snippet']['liveBroadcastContent'],
        }
        statistics_schemas = {
            "video_id": video_id,
            "view_count": detail['statistics']['viewCount'],
            "like_count": detail['statistics'].get('likeCount', 0),
            "dislike_count": detail['statistics'].get('dislikeCount', 0),
            "favorite_count": detail['statistics']['favoriteCount'],
            "comment_count": detail['statistics'].get('commentCount', 0),
        }
        snippet_model = VideoDetail(**snippet_schemas)
        statistics_model = VideoStatistics(**statistics_schemas)
        snippet_ORM.append(snippet_model)
        statistics_ORM.append(statistics_model)
        progress += 1
        print(round(progress / len(video_list), 4) * 100)

    try:
        with app.app_context():
            db.session.add_all(snippet_ORM)
            db.session.commit()
        pass
    except SQLAlchemyError as e:
        print("snippet:{}".format(type(e)))
        return False

    try:
        with app.app_context():
            db.session.add_all(statistics_ORM)
            db.session.commit()
    except SQLAlchemyError as e:
        print("statistics:{}".format(type(e)))
        return False

    return True


def save_video_statistics(video_id: str):
    popular_video = videos.get_video_detail(video_id)
    if not popular_video.get('items'):
        return False
    channel_id = popular_video['items'][0]['snippet']['channelId']

    if not check_video_exist(video_id):
        save_channel_videoid(channel_id=channel_id, video_id=video_id)

    detail = popular_video['items'][0]
    statistics_schemas = {
        "video_id": video_id,
        "view_count": detail['statistics'].get('viewCount', 0),
        "like_count": detail['statistics'].get('likeCount', 0),
        "dislike_count": detail['statistics'].get('dislikeCount', 0),
        "favorite_count": detail['statistics'].get('favoriteCount', 0),
        "comment_count": detail['statistics'].get('commentCount', 0),
    }
    statistics_model = VideoStatistics(**statistics_schemas)

    try:
        with app.app_context():
            db.session.add(statistics_model)
            db.session.commit()
    except SQLAlchemyError as e:
        print("statistics:{}".format(type(e)))
        return False

    return True


def save_most_popular_video(regionCode: str, videoCategoryId: int) -> bool:
    popular_video_list = []
    statistics_list = []
    popular_video = videos.foreach_most_popular_video(
        regionCode, videoCategoryId)
    if "error" in popular_video:
        return False
    popular_rank_list = [i[0] for i in popular_video]
    print("The categoryid {} have {} video".format(
        videoCategoryId, len(popular_video)))

    for channel_video in popular_video:
        statistics_schemas = {
            "video_id": channel_video[0],
            "view_count": channel_video[2].get('viewCount', 0),
            "like_count": channel_video[2].get('likeCount', 0),
            "dislike_count": channel_video[2].get('dislikeCount', 0),
            "favorite_count": channel_video[2].get('favoriteCount', 0),
            "comment_count": channel_video[2].get('commentCount', 0),
        }
        statistics_list.append(VideoStatistics(**statistics_schemas))

        if not check_video_exist(channel_video[0]):
            schemas = {
                "channel_id": channel_video[1]['channelId'],
                "video_id": channel_video[0]
            }
            playlist_item = ChannelPlaylistItem(**schemas)
            try:
                with app.app_context():
                    db.session.add(playlist_item)
                    db.session.commit()
            except SQLAlchemyError as e:
                print("playlist item video error:{}".format(type(e)))

    for video_id in popular_rank_list:
        popular_schemas = {
            "video_id": video_id,
            "rank": popular_rank_list.index(video_id),
            "category_id": videoCategoryId,
            "region_code": regionCode
        }
        popular_model = MostPopular(**popular_schemas)
        popular_video_list.append(popular_model)

    try:
        with app.app_context():
            db.session.add_all(popular_video_list)
            db.session.add_all(statistics_list)
            db.session.commit()
            return True
    except SQLAlchemyError as e:
        print("most popular video error:{}".format(type(e)))
        return False
