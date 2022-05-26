import tweepy
from datas.models import  Record


class TweetGenerator:
    # 相關ID
    consumer_key =  'amSmSy40cML0QBA9lKAjjlzBI'
    consumer_secret = 'qyYe2rQQB7E0Tz79flPEQKyIJKBslOPguFzmGRqOrLmQA8Gv2C'
    access_token = '1523316603772760067-OWV0wkLtbI1gV5oxAhIstLNC88whJN'
    access_token_secret =  '8AjJTofWgRqRlbmrcx2r3K3WKOArfGYXqpMWx28DMEMQn'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit = True)

    def profile_image(self, filename):
        self.api.update_profile_image(filename)

    def update_profile_info(self, name, url, location, description):
        self.api.update_profile(name, url, location, description)

    def post_tweet(self, text):
        self.api.update_status(text)

    def upload_media(self, text, filename):
        media = self.api.media_upload(filename)
        self.api.update_status(text, media_ids = [media.media_id_string])

    def post_weekly_singer_rank_tweet(self, date):
        has_find , previous_date = Record.get_previous_date(date)
        date_duration = "{} ~ {}".format(previous_date, date)

        text = "Top Hololive Singer. \nWeekly view from {}.\n #holosongranker #hololive".format(date_duration)
        filename = "datas/img/singer_rank_{}.png".format(date)

        self.upload_media(text, filename)


    def post_weekly_song_rank_tweet(self, date):
        has_find , previous_date = Record.get_previous_date(date)
        date_duration = "{} ~ {}".format(previous_date, date)

        text = "Top Hololive Song. \nWeekly view from {}.\n #holosongranker #hololive".format(date_duration)
        filename = "datas/img/song_rank_{}.png".format(date)

        self.upload_media(text, filename)


