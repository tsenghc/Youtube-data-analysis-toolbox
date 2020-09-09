from app import app
from .storage.channel_storage import save_channel_subscription
from app.models import ChannelList


def test_query(channel):
    with app.app_context():
        ChannelList.query.get(1)


if __name__ == '__main__':
    #app.run()
    #test_query("UCPRWWKG0VkBA0Pqa4Jr5j0Q")
    save_channel_subscription("UCPRWWKG0VkBA0Pqa4Jr5j0Q")
