import unittest

from crawler import subscriptions, channels


class crawlers(unittest.TestCase):
    def setUp(self) -> None:
        self.channel_list = ["UCIF_gt4BfsWyM_2GOcKXyEQ", "UC8TtAsZE51ekqffnNASo7DA", "UCAfAQOlKYd6ECvqEMiMrjaA"]

    def test_subscriptions(self):
        for channel in self.channel_list:
            result = subscriptions.foreach_subscriber_by_channel(channel)
            result = isinstance(result, list) or isinstance(result, int)
            self.assertTrue(result)

    def test_channels_detail(self):
        for channel in self.channel_list:
            result = isinstance(channels.get_channel_detail(channel), dict)
            self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
