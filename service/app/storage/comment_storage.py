from app import app
from sqlalchemy.exc import SQLAlchemyError

from service.app.crawler import comments
from service.app.models import TopLevelComment, RepliesComments, db


def save_video_comments(video_id: str) -> bool:
    """儲存影片所有留言至資料庫

    Returns:
        [bool]:
    """
    top_snippet_ORM = []
    replies_snippet_ORM = []
    video_comments = comments.foreach_video_comments(video_id)
    if not video_comments:
        return False

    for comment in video_comments['top_comments_list']:
        top_snippet_schemas = {
            "comment_id": comment['id'],
            "video_id": comment['snippet']['videoId'],
            "text_original": comment['snippet']['textOriginal'],
            "author_display_name": comment['snippet']['authorDisplayName'],
            "author_channel_id": comment['snippet']['authorChannelId']['value'],
            "like_count": comment['snippet']['likeCount'],
            "published_at": comment['snippet']['publishedAt'],
            "updated_at": comment['snippet']['updatedAt']
        }
        top_snippet_ORM.append(TopLevelComment(**top_snippet_schemas))
    for replies in video_comments['replies_comments_list']:
        for comment in replies:
            replies_snippet_schemas = {
                "comments_id": comment['id'],
                "parent_id": comment['snippet']['parentId'],
                "video_id": comment['snippet']['videoId'],
                "text_original": comment['snippet']['textOriginal'],
                "author_display_name": comment['snippet']['authorDisplayName'],
                "author_channel_id": comment['snippet']['authorChannelId']['value'],
                "like_count": comment['snippet']['likeCount'],
                "published_at": comment['snippet']['publishedAt'],
                "updated_at": comment['snippet']['updatedAt']
            }
            replies_snippet_ORM.append(RepliesComments(**replies_snippet_schemas))

    try:
        with app.app_context():
            db.session.add_all(top_snippet_ORM)
            db.session.commit()
    except SQLAlchemyError as e:
        print("top_comment:{}".format(type(e)))

    try:
        with app.app_context():
            db.session.add_all(replies_snippet_ORM)
            db.session.commit()
    except SQLAlchemyError as e:
        print("replies_comment:{}".format(type(e)))


if __name__ == '__main__':
    save_video_comments('jC0cxlW681I')
    pass
