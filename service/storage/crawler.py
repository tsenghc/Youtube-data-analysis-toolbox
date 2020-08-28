from service.storage.models import Subscriptions
from service.crawler import subscriptions, channels


def relate_channel(channel_id: str) -> True:
    channel_list = subscriptions.foreach_subscriber_by_channel(channel_id)
    for channel in channel_list:
        channel_detail = channels.get_channel_detail(channel)
        subscript_model = Subscriptions(
            resourceChannelId=channel,
            originalChannelId=channel_id,
            subscriptAt=channel_detail["items"][0]["snippet"]["publishedAt"],
            resourceTitle=channel_detail["items"][0]["snippet"]["title"],
            resourceDescription=channel_detail["items"][0]["snippet"]["description"]
        )
        try:
            subscript_model.save_to_db()
            print(subscript_model)
        except:
            pass



if __name__ == '__main__':
    relate_channel("UCPRWWKG0VkBA0Pqa4Jr5j0Q")
