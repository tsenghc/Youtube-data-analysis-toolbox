import falcon

from views import server
from views import channel

app = falcon.API()
app.add_route('/server/info', server.ServerStatus())
app.add_route('/channel/{channel_id}', channel.ChannelDetail())
app.add_route('/subscribed/{channel_id}', channel.ChannelSubscribed())
