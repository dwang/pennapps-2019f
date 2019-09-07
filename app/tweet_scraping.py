import GetOldTweets3 as got
import datetime

class TweetScraper:
    def __init__(self, query, start_date, end_date):
        self.query = query
        self.start_date = start_date
        self.end_date = end_date

    def get_tweets(self):
        tweetCriteria = got.manager.TweetCriteria().setQuerySearch(self.query).setSince(self.start_date).setUntil(self.end_date).setTopTweets(True).setMaxTweets(100)

        tweets = []
        for tweet in got.manager.TweetManager.getTweets(tweetCriteria):
            tweets.append(tweet.text)

        return tweets
