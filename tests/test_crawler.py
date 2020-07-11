import unittest

from crawler import subscriptions, channels, playlists, playlistItem


class crawlers(unittest.TestCase):
    def setUp(self) -> None:
        self.channel_list = ["UCIF_gt4BfsWyM_2GOcKXyEQ", "UC8TtAsZE51ekqffnNASo7DA", "UCAfAQOlKYd6ECvqEMiMrjaA",
                             "UC1ppNp9vab0qlkUWZvnLl0A", "UCnJEWsS5agXCkqIpyHC9Grg", "UCK3Ycl9dcHk0qz8yoN-6phA",
                             "UC-lHJZR3Gqxm24_Vd_AJ5Yw"]

    def test_subscriptions(self):
        for channel in self.channel_list:
            result = subscriptions.foreach_subscriber_by_channel(channel)
            print(result)
            result = isinstance(result, list) or isinstance(result, int)
            self.assertTrue(result)

    def test_channels_detail(self):
        for channel in self.channel_list:
            result = channels.get_channel_detail(channel)
            print(result)
            result = isinstance(result, dict)
            self.assertTrue(result)

    def test_get_all_playlist(self):
        for channel in self.channel_list:
            result = playlists.foreach_playlistId_by_channel(channelId=channel)
            print(result)
            result = isinstance(result, list) or isinstance(result, int)
            self.assertTrue(result)

    def test_get_playlist_video(self):
        for channel in self.channel_list:
            channel_detail = channels.get_channel_detail(channel)
            channel_playlist = channel_detail["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            result = playlistItem.foreach_playlist_videoId(channel_playlist)
            print("channel:{},VideoCount:{}".format(channel, len(result)))
            result = isinstance(result, list)
            self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
