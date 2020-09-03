from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func

db = SQLAlchemy()
db.init_app(app)


class Subscriptions(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, nullable=False)
    resource_channel_id = db.Column(db.String(24), index=True, unique=True, nullable=False)
    original_channel_id = db.Column(db.String(24),
                                    ForeignKey("channel_list.channel_id"),
                                    nullable=False)
    subscript_at = db.Column(db.DateTime, nullable=False)
    update_time = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, **kwargs):
        super(Subscriptions, self).__init__(**kwargs)


class ChannelList(db.Model):
    __tablename__ = 'channel_list'
    channel_id = db.Column(db.String(24), nullable=False, primary_key=True, index=True, unique=True)

    def __init__(self, **kwargs):
        super(ChannelList, self).__init__(**kwargs)


class ChannelSnippet(db.Model):
    __tablename__ = 'channel_snippet'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, nullable=False)
    channel_id = db.Column(db.String(24),
                           ForeignKey("channel_list.channel_id"),
                           nullable=False)
    channel_title = db.Column(db.String(100), nullable=False)
    channel_description = db.Column(db.String(1000), nullable=False)
    channel_custom_url = db.Column(db.String(100), nullable=False)
    channel_published_at = db.Column(db.DateTime, nullable=False)
    channel_thumbnails_url = db.Column(db.String(200), nullable=False)
    channel_country = db.Column(db.String(2), nullable=False)
    update_time = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, **kwargs):
        super(ChannelSnippet, self).__init__(**kwargs)


class ChannelStatistics(db.Model):
    __tablename__ = 'channel_statist'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, nullable=False)
    channel_id = db.Column(db.String(24),
                           ForeignKey("channel_list.channel_id"),
                           nullable=False)
    view_count = db.Column(db.BIGINT, nullable=False, default=0)
    comment_count = db.Column(db.BIGINT, nullable=False, default=0)
    subscriber_count = db.Column(db.BIGINT, nullable=False, default=0)
    video_count = db.Column(db.BIGINT, nullable=False, default=0)
    hidden_subscriber_count = db.Column(db.BOOLEAN, nullable=False)
    update_time = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, **kwargs):
        super(ChannelStatistics, self).__init__(**kwargs)


class ChannelContentDetail(db.Model):
    __tablename__ = 'channel_content_detail'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, nullable=False)
    channel_id = db.Column(db.String(24),
                           ForeignKey("channel_list.channel_id"),
                           nullable=False)
    channel_related_playlists = db.Column(db.String(24), nullable=False)
    channel_keywords = db.Column(db.JSON)
    channel_topic_id = db.Column(db.JSON)

    def __init__(self, **kwargs):
        super(ChannelContentDetail, self).__init__(**kwargs)


class TopicIds(db.Model):
    __tablename__ = 'channel_topic'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, nullable=False)
    channel_id = db.Column(db.String(24),
                           ForeignKey("channel_list.channel_id"),
                           nullable=False)
    topic_name = db.Column(db.JSON, nullable=False)

    def __init__(self, topicName, channelId):
        self.topic_name = topicName
        self.channel_id = channelId


class Keywords(db.Model):
    __tablename__ = 'channel_keywords'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, nullable=False)
    channel_id = db.Column(db.String(24),
                           ForeignKey("channel_list.channel_id"),
                           nullable=False)
    keyword = db.Column(db.JSON, nullable=False)

    def __init__(self, keyword, channelId):
        self.keyword = keyword
        self.channel_id = channelId


class ChannelPlaylistItem(db.Model):
    __tablename__ = 'channel_playlist_items'
    video_id = db.Column(db.String(11), primary_key=True, nullable=False)
    video_published_at = db.Column(db.DateTime, nullable=False)
    channel_id = db.Column(db.String(24), nullable=False)

    def __init__(self, videoId, videoPublishedAt, channelId):
        self.video_id = videoId
        self.video_published_at = videoPublishedAt
        self.channel_id = channelId


class VideoDetail(db.Model):
    __tablename__ = 'video_detail'
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, nullable=False)
    video_id = db.Column(
        db.String(11),
        ForeignKey('channel_playlist_items.video_id'),
        nullable=False,
    )
    title = db.Column(db.String(70), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    tags = db.Column(db.JSON, nullable=False, default=None)
    category_id = db.Column(db.SMALLINT, nullable=False)
    default_audio_language = db.Column(db.String(5), nullable=False)
    live_broadcast_content = db.Column(db.String, nullable=False)

    def __init__(self, **kwargs):
        super(VideoDetail, self).__init__(**kwargs)


class VideoStatistics(db.Model):
    id = db.Column(db.BIGINT, primary_key=True, autoincrement=True, nullable=False)
    video_id = db.Column(
        db.String(11),
        ForeignKey('channel_playlist_items.video_id'),
        nullable=False,
    )
    view_count = db.Column(db.BIGINT, nullable=False, default=0)
    like_count = db.Column(db.BIGINT, nullable=False, default=0)
    dislike_count = db.Column(db.BIGINT, nullable=False, default=0)
    favorite_count = db.Column(db.BIGINT, nullable=False, default=0)
    comment_count = db.Column(db.BIGINT, nullable=False, default=0)

    def __init__(self, **kwargs):
        super(VideoStatistics, self).__init__(**kwargs)


class TopLevelComment(db.Model):
    __tablename__ = 'top_level_comment'
    comment_id = db.Column(db.String(26), primary_key=True, nullable=False)
    video_id = db.Column(db.String(11), nullable=False)
    text_original = db.Column(db.String, nullable=False)
    author_display_name = db.Column(db.String, nullable=False)
    author_channel_id = db.Column(db.String, nullable=False)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    published_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, **kwargs):
        super(TopLevelComment, self).__init__(**kwargs)


class RepliesComments(db.Model):
    __tablename__ = 'replies_comments'
    comments_id = db.Column(db.String(49), primary_key=True, nullable=False)
    parent_id = db.Column(
        db.String(26),
        ForeignKey('top_level_comment.comment_id'),
        nullable=False,
        primary_key=True
    )
    video_id = db.Column(db.String(11), nullable=False)
    text_original = db.Column(db.String, nullable=False)
    author_display_name = db.Column(db.String, nullable=False)
    author_channel_id = db.Column(db.String, nullable=False)
    like_count = db.Column(db.Integer, nullable=False, default=0)
    published_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, **kwargs):
        super(RepliesComments, self).__init__(**kwargs)
