import unittest

from src.crawler import playlists, playlistItem, comments
from src.crawler import subscriptions, channels, videos


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

    def test_get_video_detail(self):
        for channel in self.channel_list:
            channel_detail = channels.get_channel_detail(channel)
            channel_playlist = channel_detail["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            video_list = playlistItem.get_firstPage_videoId(channel_playlist, 2)
            for videoid in video_list:
                result = videos.get_video_detail(videoId=videoid)
                print(result["items"][0]["snippet"]["title"])
                result = isinstance(result, dict)
                self.assertTrue(result)

    def test_get_video_comments_text(self):
        for channel in self.channel_list:
            channel_detail = channels.get_channel_detail(channel)
            channel_playlist = channel_detail["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
            video_list = playlistItem.get_firstPage_videoId(channel_playlist, maxResult=2)
            for videoid in video_list:
                comments_result = comments.get_video_comments(videoid, maxResult=1)["items"]
                for comment in comments_result:
                    result = comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
                    print(result)
                    result = isinstance(result, str)
                    self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
