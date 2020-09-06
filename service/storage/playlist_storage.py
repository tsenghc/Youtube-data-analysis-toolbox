from app import app
from sqlalchemy.exc import SQLAlchemyError

from service.crawler import playlistItem
from service.storage.channel_storage import save_channel_detail
from service.storage.models import db, ChannelContentDetail, ChannelPlaylistItem


def check_content_exist(channel_id: str) -> bool:
    """確認頻道的ContentDetail內容是否存在
    Args:
        channel_id: Youtube channel id.
        
    Returns:
        [bool]: 
    """
    try:
        with app.app_context():
            channel = ChannelContentDetail.query.filter_by(channel_id=channel_id).first()
            if channel is None:
                save_channel_detail(channel_id)
                check_content_exist(channel_id)
            else:
                return True
    except SQLAlchemyError as e:
        print("check_content_exist:{}".format(type(e)))
        return False


def save_channel_playlist_items(channel_id: str) -> bool:
    """儲存該頻道所有的影片ID
    Args:
        channel_id: Youtube channel id.

    Returns:
        [bool]:
    """
    if check_content_exist(channel_id):
        with app.app_context():
            query = db.session.query(
                ChannelContentDetail.channel_related_playlists).filter_by(
                channel_id=channel_id).first()
            channel_related_playlists = query[0]
        video_list = playlistItem.foreach_playlist_videoId(channel_related_playlists)

        playlist_ORM = []
        for video_id in video_list:
            schemas = {
                "video_id": video_id,
                "channel_id": channel_id
            }
            play_list_model = ChannelPlaylistItem(**schemas)
            playlist_ORM.append(play_list_model)

        try:
            with app.app_context():
                db.session.add_all(playlist_ORM)
                db.session.commit()
                return True
        except SQLAlchemyError as e:
            print(type(e))
    return False


if __name__ == '__main__':
    save_channel_playlist_items("UCPRWWKG0VkBA0Pqa4Jr5j0Q")
