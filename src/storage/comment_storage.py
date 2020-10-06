from sqlalchemy import util
from .flask_app import create_app
from sqlalchemy.exc import SQLAlchemyError
from crawler import comments
from models.model import TopLevelComment, RepliesComments, db
from sqlalchemy import distinct
from utils.storage import pgsql_0x00_repleace
app = create_app('development')


def save_video_comments(video_id: str) -> bool:
    """儲存影片所有留言至資料庫

    Returns:
        [bool]:
    """
    commit_status = {}
    top_comment_insert_count = 0
    replies_comment_insert_count = 0
    comment = comments.foreach_video_comments(video_id)

    if not comment or comment.get('error'):
        return comment

    video_top_comments = comment['top_comments_list']
    video_replies_comments = comment['replies_comments_list']
    top_exist_comment_id = exist_top_comment_id()
    replies_exist_comment_id = replies_comment_id()
    print("This video have {} TopComments|{} repliesComments".format(
        len(video_top_comments), len(video_replies_comments)))

    for comment in video_top_comments:
        if comment['id'] not in top_exist_comment_id:
            top_snippet_schemas = {
                "comment_id": comment['id'],
                "video_id": comment['snippet']['videoId'],
                "text_original": comment['snippet']['textOriginal'],
                "author_display_name": comment['snippet']['authorDisplayName'],
                "author_channel_id": comment['snippet'].get('authorChannelId', {}).get('value', "unknow"),
                "like_count": comment['snippet']['likeCount'],
                "published_at": comment['snippet']['publishedAt'],
                "updated_at": comment['snippet']['updatedAt']
            }
            top_snippet_schemas = pgsql_0x00_repleace(top_snippet_schemas)
            try:
                with app.app_context():
                    db.session.add(TopLevelComment(**top_snippet_schemas))
                    db.session.commit()
                    top_comment_insert_count += 1
                    commit_status["top_snippet"] = (
                        True, top_comment_insert_count)
            except SQLAlchemyError as e:
                print("top_comment:{}".format(type(e.args[0])))
                commit_status["top_snippet"] = False

    for comment in recursive_replies(video_replies_comments):
        if comment['id'] not in replies_exist_comment_id:
            replies_snippet_schemas = {
                "comments_id": comment['id'],
                "parent_id": comment['snippet']['parentId'],
                "video_id": comment['snippet']['videoId'],
                "text_original": comment['snippet']['textOriginal'],
                "author_display_name": comment['snippet']['authorDisplayName'],
                "author_channel_id": comment['snippet'].get('authorChannelId', {}).get('value', "unknow"),
                "like_count": comment['snippet']['likeCount'],
                "published_at": comment['snippet']['publishedAt'],
                "updated_at": comment['snippet']['updatedAt']
            }
            replies_snippet_schemas = pgsql_0x00_repleace(
                replies_snippet_schemas)
            try:
                with app.app_context():
                    db.session.add(RepliesComments(
                        **replies_snippet_schemas))
                    db.session.commit()
                    replies_comment_insert_count += 1
                    commit_status["replies_snippet"] = (
                        True, replies_comment_insert_count)
            except SQLAlchemyError as e:
                print("replies_comment:{}".format(type(e.args[0])))
                commit_status["replies_snippet"] = False

    return commit_status


def recursive_replies(replies_comments):
    """遍歷所有回復的留言到清單中

    Args:
        replies_comments ([str]]): [第二層回復的留言]

    Returns:
        [list]]: [將裡層的留言遍歷到清單表層]
    """
    comment = []
    for k, v in enumerate(replies_comments):
        if isinstance(v, list):
            for j in v:
                comment.append(j)
        else:
            comment.append(v)
    return comment


def exist_top_comment_id():
    """[取得已儲存的表層留言ID]

    Returns:
        [list]]: [留言內容]
    """
    try:
        with app.app_context():
            comment_id = TopLevelComment.query.with_entities(
                distinct(TopLevelComment.comment_id)).all()
            res = [i for (i,) in comment_id]
            return res
    except SQLAlchemyError as e:
        print("exsite_top_comment_id:{}".format(type(e.args[0])))
    return False


def replies_comment_id():
    """[取得已儲存的裡層留言ID]

    Returns:
        [list]]: [留言內容]
    """
    try:
        with app.app_context():
            comment_id = RepliesComments.query.with_entities(
                distinct(RepliesComments.comments_id)).all()
            res = [i for (i,) in comment_id]
            return res
    except SQLAlchemyError as e:
        print("replies_top_comment_id:{}".format(type(e.args[0])))
    return False
