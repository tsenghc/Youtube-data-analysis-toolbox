from app import app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()
db.init_app(app)


class Subscriptions(db.Model):
    __tablename__ = 'subscriptions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resourceChannelId = db.Column(db.String(30), primary_key=False, nullable=False)
    originalChannelId = db.Column(db.String(30), nullable=False)
    subscriptAt = db.Column(db.DateTime, nullable=False)
    resourceTitle = db.Column(db.String(255), nullable=False)
    resourceDescription = db.Column(db.String(1000), nullable=True)
    writeTime = db.Column(db.DateTime, default=func.now(), nullable=False)

    def __init__(self, resourceChannelId,
                 originalChannelId, subscriptAt,
                 resourceTitle, resourceDescription,
                 writeTime):
        self.resourceChannelId = resourceChannelId
        self.originalChannelId = originalChannelId
        self.subscriptAt = subscriptAt
        self.resourceTitle = resourceTitle
        self.resourceDescription = resourceDescription
        self.writeTime = writeTime

    def batch_save_to_db(self, channel_list):
        with app.app_context():
            db.session.add_all(channel_list)
            db.session.commit()
