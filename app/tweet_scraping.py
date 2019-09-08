import GetOldTweets3 as got
import sentiment_analysis
import content_classification
import datetime


def get_tweets(query, start_date, end_date):
    tweet_criteria = got.manager.TweetCriteria().setQuerySearch(query).setSince(
        start_date).setUntil(end_date).setTopTweets(True).setMaxTweets(1)

    overall_sentiment_score = 0.0

    for tweet in got.manager.TweetManager.getTweets(tweet_criteria):
        try:
            sentiment = sentiment_analysis.analyze(tweet.text)[0]
            category = content_classification.classify(tweet.text)

            if category == "News/Politics" or category == "/Finance/Investing":
                sentiment.score *= 1.5

            overall_sentiment_score += sentiment.score
            print(f"{tweet.text}: {category} {sentiment.score}\n")
        except Exception as e:
            print(f"Exception: {e}")
            pass

    return overall_sentiment_score

if __name__ == "__main__":
    print(get_tweets("AAPL", "2019-09-01", "2019-09-03"))
