import falcon

from views import server
from views import channel

app = falcon.API()
app.add_route('/server', server.ServerStatus())
app.add_route('/channel/{channel_id}',channel.ChannelDetail())
