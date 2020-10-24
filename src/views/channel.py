import json

import falcon
from crawler import channels
from storage import channel_storage
from database import db_channel


class ChannelDetail:
    def on_get(self, req, resp, channel_id):
        res = db_channel.get_db_channel_detail(channel_id=channel_id)
        resp.status = falcon.HTTP_200
        if res.get('error'):
            resp.status = falcon.HTTP_404
        resp.body = json.dumps(res)


class ChannelSubscribed:
    def on_get(self, req, resp, channel_id):
        res = db_channel.get_db_channel_subscribed(channel_id=channel_id)
        if isinstance(res, dict):
            if res.get('error') or res.get('result'):
                resp.status = falcon.HTTP_404
        else:
            resp.body = json.dumps(res)
            resp.status = falcon.HTTP_200
