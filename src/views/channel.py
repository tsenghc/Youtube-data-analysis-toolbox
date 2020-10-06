import json

import falcon
from crawler import channels
from storage import channel_storage
from database import db_channel


class ChannelDetail:
    def on_get(self, req, resp, channel_id):
        print(req)
        res = db_channel.get_db_channel_detail(channel_id=channel_id)
        resp.status = falcon.HTTP_200
        if res.get('error'):
            resp.status = falcon.HTTP_404
        resp.body = json.dumps(res)
