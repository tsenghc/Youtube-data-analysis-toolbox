from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.sql import func

db = SQLAlchemy()
db.init_app(app)


class Subscriptions(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resourceChannelId = db.Column(db.String(24), primary_key=False, nullable=False)
    originalChannelId = db.Column(db.String(24), nullable=False)
    subscriptAt = db.Column(db.DateTime, nullable=False)
    resourceTitle = db.Column(db.String(100), nullable=False)
    resourceDescription = db.Column(db.String(1000), nullable=True)
    writeTime = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self,
                 resourceChannelId, originalChannelId,
                 subscriptAt, resourceTitle,
                 resourceDescription, writeTime):
        self.resourceChannelId = resourceChannelId
        self.originalChannelId = originalChannelId
        self.subscriptAt = subscriptAt
        self.resourceTitle = resourceTitle
        self.resourceDescription = resourceDescription
        self.writeTime = writeTime

    @staticmethod
    def batch_save_to_db(channel_list):
        with app.app_context():
            db.session.add_all(channel_list)
            db.session.commit()


class ChannelDetail(db.Model):
    __tablename__ = 'channel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    channelId = db.Column(db.String(24), nullable=False)
    channelTitle = db.Column(db.String(100), nullable=False)
    channelDescription = db.Column(db.String(100), nullable=False)
    channelCustomUrl = db.Column(db.String(1000), nullable=False)
    channelPublishedAt = db.Column(db.DateTime, nullable=False)
    channelThumbnailsUrl = db.Column(db.String(200), nullable=False)
    channelCountry = db.Column(db.String(2), nullable=False)
    channelRelatedPlaylists = db.Column(db.String(24), nullable=False)
    channelViewCount = db.Column(db.Integer)
    channelCommentCount = db.Column(db.Integer)
    channelVideoCount = db.Column(db.Integer)
    channelKeywords = db.Column(db.ARRAY(db.String))
    channelTopicIds = db.Column(db.String(10))

    def __init__(self,
                 channelId, channelTitle,
                 channelDescription, channelCustomUrl,
                 channelPublishedAt, channelThumbnailsUrl,
                 channelCountry, channelRelatedPlaylists,
                 channelViewCount, channelCommentCount,
                 channelVideoCount, channelKeywords,
                 channelTopicIds):
        self.channelId = channelId
        self.channelTitle = channelTitle
        self.channelDescription = channelDescription
        self.channelCustomUrl = channelCustomUrl
        self.channelPublishedAt = channelPublishedAt
        self.channelThumbnailsUrl = channelThumbnailsUrl
        self.channelCountry = channelCountry
        self.channelRelatedPlaylists = channelRelatedPlaylists
        self.channelViewCount = channelViewCount
        self.channelCommentCount = channelCommentCount
        self.channelVideoCount = channelVideoCount
        self.channelKeywords = channelKeywords
        self.channelTopicIds = channelTopicIds


class TopicIds(db.Model):
    __tablename__ = 'topic_id'
    id = db.Column(db.String(10), primary_key=True, nullable=False)
    topicName = db.Column(db.String, nullable=False)

    def __init__(self, topicName):
        self.topicName = topicName


class Keywords(db.Model):
    __tablename__ = 'channelKeywords'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keyword = db.Column(db.String(20), nullable=False)

    def __init__(self, keyword):
        self.keyword = keyword


class ChannelPlaylistItem(db.Model):
    __tablename__ = 'channel_playlist_items'
    videoId = db.Column(db.String(11), primary_key=True, nullable=False)
    videoPublishedAt = db.Column(db.DateTime, nullable=False)
    channelId = db.Column(db.String(24), nullable=False)

    def __init__(self, videoId, videoPublishedAt, channelId):
        self.videoId = videoId
        self.videoPublishedAt = videoPublishedAt
        self.channelId = channelId


class VideoDetail(db.Model):
    __tablename__ = 'video_detail'
    videoId = db.Column(
        db.String(11),
        ForeignKey('channel_playlist_items.videoId'),
        nullable=False,
        primary_key=True
    )
    title = db.Column(db.String(70), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    tags = db.Column(db.ARRAY(db.String))
    categoryId = db.Column(db.Integer)
    defaultAudioLanguage = db.Column(db.String(5))
    liveBroadcastContent = db.Column(db.String())
    viewCount = db.Column(db.Integer)
    likeCount = db.Column(db.Integer)
    dislikeCount = db.Column(db.Integer)
    favoriteCount = db.Column(db.Integer)
    commentCount = db.Column(db.Integer)

    def __init__(self,
                 videoId, title,
                 description, tags,
                 categoryId, defaultAudioLanguage,
                 liveBroadcastContent, viewCount,
                 likeCount, dislikeCount,
                 favoriteCount, commentCount):
        self.videoId = videoId
        self.title = title
        self.description = description
        self.tags = tags
        self.categoryId = categoryId
        self.defaultAudioLanguage = defaultAudioLanguage
        self.liveBroadcastContent = liveBroadcastContent
        self.viewCount = viewCount
        self.likeCount = likeCount
        self.dislikeCount = dislikeCount
        self.favoriteCount = favoriteCount
        self.commentCount = commentCount
