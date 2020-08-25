from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
db.init_app(app)


class Subscriptions(db.Model):
    __tablename__ = 'subscriptions'
    resourceChannelId = db.Column(db.String(30), primary_key=True)
    originalChannelId = db.Column(db.String(30), nullable=False)
    subscriptAt = db.Column(db.DateTime)
    resourceTitle = db.Column(db.String(255), nullable=False)
    resourceDescription = db.Column(db.String(1000), nullable=True)

    def __init__(self, resourceChannelId, originalChannelId, subscriptAt, resourceTitle, resourceDescription):
        self.resourceChannelId = resourceChannelId
        self.originalChannelId = originalChannelId
        self.subscriptAt = subscriptAt
        self.resourceTitle = resourceTitle
        self.resourceDescription = resourceDescription

    def save_to_db(self):
        with app.app_context():
            db.session.add(self)
            db.session.commit()
