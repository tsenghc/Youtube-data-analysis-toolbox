import json

import falcon
from crawler import channels
from storage import channel_storage


class ChannelDetail:
    def on_get(self, req, resp, channel_id):
        tt = channels.get_channel_detail(channelId=channel_id)
        channel_storage.save_channel_subscription(channel_id=channel_id)
        resp.status = falcon.HTTP_200
        resp.body = json.dumps(tt)
