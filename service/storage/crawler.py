from datetime import datetime

from app import app

from service.crawler import subscriptions, channels
from service.storage.models import Subscriptions, db


def subscription_channel(channel_id: str) -> bool:
    """該頻道訂閱的公開使用者

    Args:
        channel_id: Youtube channel id.

    Returns:
        [bool]:The true if success else fail.

    """
    subscribed_ORM = []
    user_public_subscription_list = \
        subscriptions.foreach_subscriber_by_channel(channel_id)

    print("This channel subscription user have {}".format(
        len(user_public_subscription_list)))

    for channel in user_public_subscription_list:
        channel_detail = channels.get_channel_detail(
            channel)["items"][0]["snippet"]
        subscript_model = Subscriptions(
            resourceChannelId=channel,
            originalChannelId=channel_id,
            subscriptAt=channel_detail["publishedAt"],
            resourceTitle=channel_detail["title"],
            resourceDescription=channel_detail["description"],
            writeTime=datetime.utcnow()
        )
        subscribed_ORM.append(subscript_model)

    try:
        with app.app_context():
            db.session.add_all(subscribed_ORM)
            db.session.commit()

        return True
    except Exception:
        print(Exception)

    return False


if __name__ == '__main__':
    subscription_channel("UCPRWWKG0VkBA0Pqa4Jr5j0Q")
    pass
