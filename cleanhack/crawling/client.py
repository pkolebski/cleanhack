import os
import ssl
from pathlib import Path

import click
import pandas as pd
import tweepy

ssl._create_default_https_context = ssl._create_unverified_context

CONSUMER_KEY = "dgljcMV4eVGIvC4G16YHkrxUC"
CONSUMER_SECRET = "choJ7oxvOmYz0yxFtVWAZqOEBNISSEFjUuO9xPFFJneZIREi2Y"
ACCESS_TOKEN = "603508578-eFpY0qdZjaqgijVOSEXhzgOG5AF7WAiiPstcAC0e"
ACCESS_TOKEN_SECRET = "w6f0SwqZkX9Ew6mNZihF6AWzYFJN1FPvvivXltlbaJ4Np"
FILENAME = 'crawled_users.json'
SAVE_TO_DIR = os.path.join(Path(__file__).parent.parent, 'data/crawled_users/')


class TwitterClient(object):
    def __init__(self, consumer_key, consumer_secret, access_token, access_token_secret):
        try:
            # OAuthHandler object
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

        except tweepy.TweepError as e:
            print(f"Error: Twitter Authentication Failed - \n{str(e)}")

            # Function to fetch tweets

    def get_tweets(self, query, lang='en', result_type='popular', max_tweets=10):
        # empty list to store parsed tweets
        tweets = []
        tweet_count = 0

        while tweet_count < max_tweets:
            try:
                new_tweets = self.api.search(q=query, lang=lang, result_type=result_type,
                                             count=max_tweets)
                if not new_tweets:
                    print("No more tweets found")
                    break

                for tweet in new_tweets:
                    parsed_tweet = {
                        'id': tweet.id,
                        'tweets': tweet.text,
                        'user_id': tweet.user.id
                    }
                    # appending parsed tweet to tweets list
                    if tweet.retweet_count > 0:
                        # if tweet has retweets, ensure that it is appended only once
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                    else:
                        tweets.append(parsed_tweet)
                tweet_count += len(new_tweets)
                print("Downloaded {0} tweets".format(tweet_count))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                print("Tweepy error : " + str(e))
                break
        return pd.DataFrame(tweets)

    def get_user_tweets(self, user_id, max_tweets=10):
        # empty list to store parsed tweets
        tweets = []
        tweet_count = 0

        while tweet_count < max_tweets:
            try:
                new_tweets = self.api.user_timeline(id=user_id, count=max_tweets)
                if not new_tweets:
                    print("No more tweets found")
                    break

                for tweet in new_tweets:
                    parsed_tweet = {
                        'id': tweet.id,
                        'text': tweet.text,
                        'created_at': tweet.created_at,
                        'hashtags': ', '.join(ht['text'] for ht in tweet.entities['hashtags'])
                    }
                    if tweet.entities['user_mentions']:
                        parsed_tweet['user_mentions'] = \
                            [(um['name'], um['id']) for um in tweet.entities['user_mentions']]
                    else:
                        parsed_tweet['user_mentions'] = ''
                    if tweet.entities['urls']:
                        parsed_tweet['urls'] = \
                            [(u['url'], u['expanded_url']) for u in tweet.entities['urls']]
                    else:
                        parsed_tweet['urls'] = ''
                    # user
                    parsed_tweet['user_id'] = tweet.user.id
                    parsed_tweet['user_name'] = tweet.user.name
                    parsed_tweet['user_location'] = tweet.user.location
                    parsed_tweet['user_description'] = tweet.user.description
                    parsed_tweet['user_followers_count'] = tweet.user.followers_count
                    parsed_tweet['user_friends_count'] = tweet.user.friends_count
                    parsed_tweet['user_created_at'] = tweet.user.created_at
                    parsed_tweet['user_favourites_count'] = tweet.user.favourites_count
                    parsed_tweet['user_statuses_count'] = tweet.user.statuses_count
                    parsed_tweet['user_profile_image_url'] = tweet.user.profile_image_url
                    parsed_tweet['user_profile_background_image_url'] = tweet.user.profile_image_url
                    # stats
                    parsed_tweet['geo'] = tweet.geo
                    parsed_tweet['place'] = tweet.place
                    parsed_tweet['is_quote_status'] = tweet.is_quote_status
                    parsed_tweet['retweet_count'] = tweet.retweet_count
                    parsed_tweet['favorite_count'] = tweet.favorite_count

                    tweets.append(parsed_tweet)
                    # appending parsed tweet to tweets list
                    if tweet.retweet_count > 0:
                        # if tweet has retweets, ensure that it is appended only once
                        if parsed_tweet not in tweets:
                            tweets.append(parsed_tweet)
                    else:
                        tweets.append(parsed_tweet)
                tweet_count += len(new_tweets)
                print("Downloaded {0} tweets".format(tweet_count))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                print("Tweepy error : " + str(e))
                break
        return pd.DataFrame(tweets)

    def get_users_data_by_query(self, query, lang, result_type, max_tweets_query, max_tweets_user,
                                max_users):
        query_tweets = self.get_tweets(query, lang, result_type, max_tweets_query)
        query_tweets_id_list = query_tweets['user_id'].unique()
        top_user_ids = query_tweets_id_list[:max_users]
        user_tweets = []
        for user_id in top_user_ids:
            user_tweets.append(self.get_user_tweets(user_id, max_tweets_user))
        user_tweets = pd.concat(user_tweets)
        user_tweets = user_tweets.drop_duplicates(subset=['id'])
        user_tweets = user_tweets.reset_index(drop=True)
        return user_tweets


@click.command()
@click.option('--query', '-q',
              type=click.STRING,
              default="renewables, renewableenergy",
              help="Search query to be scrapped")
@click.option('--lang', '-l',
              type=click.STRING,
              default='en',
              help="Language of tweets to be scrapped")
@click.option('--result-type', '-rt',
              type=click.STRING,
              default='popular',
              help="One of popular/recent/mixed")
@click.option('--max-tweets-query', '-mtq',
              type=click.INT, default=30,
              help="Maxmimum number of tweets scraped by the query")
@click.option('--max-tweets-user', '-mtu',
              type=click.INT, default=30,
              help="Maxmimum number of tweets scraped from user's profile")
@click.option('--max-users', '-mu',
              type=click.INT, default=20,
              help="Maxmimum number of users for the analysis")
@click.option('--output', '-o',
              type=click.STRING,
              default=SAVE_TO_DIR,
              help="Output filepath")
@click.option('--filename', '-f',
              type=click.STRING,
              default=FILENAME,
              help="Output filename")
def crawl_top_users_tweets(query, lang, result_type, max_tweets_query, max_tweets_user,
                           max_users, output, filename):
    client = TwitterClient(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token=ACCESS_TOKEN,
        access_token_secret=ACCESS_TOKEN_SECRET)

    user_tweets_data = client.get_users_data_by_query(
        query=query,
        lang=lang,
        result_type=result_type,
        max_tweets_query=max_tweets_query,
        max_tweets_user=max_tweets_user,
        max_users=max_users)

    print(f"Saving to {output}")
    if not os.path.exists(output):
        os.makedirs(output)
    user_tweets_data.to_json(os.path.join(output, filename))


crawl_top_users_tweets()
