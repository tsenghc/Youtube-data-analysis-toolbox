from app import app
from app.crawler import videos
from app.models import ChannelPlaylistItem, VideoDetail, VideoStatistics, db, MostPopular
from app.storage.playlist_storage import save_channel_playlist_items, save_channel_videoid
from sqlalchemy.exc import SQLAlchemyError


def check_video_exist(video_id: str) -> bool:
    """確認該影片是否存在於PlaylistItem欄位中

    Returns:
        [bool]:
    """
    try:
        with app.app_context():
            video = ChannelPlaylistItem.query.filter_by(video_id=video_id).first()
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
            query = ChannelPlaylistItem.query.filter_by(channel_id=channel_id).all()
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
    channel_id = popular_video['items'][0]['snippet']['channelId']

    if not check_video_exist(video_id):
        save_channel_videoid(channel_id=channel_id, video_id=video_id)

    detail = popular_video['items'][0]
    statistics_schemas = {
        "video_id": video_id,
        "view_count": detail['statistics']['viewCount'],
        "like_count": detail['statistics'].get('likeCount', 0),
        "dislike_count": detail['statistics'].get('dislikeCount', 0),
        "favorite_count": detail['statistics']['favoriteCount'],
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


def save_most_popular_video(regionCode: str, videoCategoryId: int):
    popular_video_list = []
    popular_video = videos.foreach_most_popular_video(regionCode, videoCategoryId)
    for video_id in popular_video:
        if not check_video_exist(video_id):
            save_video_statistics(video_id)
        popular_schemas = {
            "video_id": video_id,
            "rank": popular_video.index(video_id)
        }
        popular_model = MostPopular(**popular_schemas)
        popular_video_list.append(popular_model)

    try:
        with app.app_context():
            db.session.add_all(popular_video_list)
            db.session.commit()
    except SQLAlchemyError as e:
        print("statistics:{}".format(type(e)))
        return False

    return True


if __name__ == '__main__':
    print(save_channel_video_detail("UC_XRq7JriAORvDe1lI1RAsA"))

pass
