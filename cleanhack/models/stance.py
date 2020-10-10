import pandas as pd

from cleanhack.models.base import Model


class Stance(Model):
    def predict(self, tweets: pd.DataFrame, *args, **kwargs):
        outputs = []
        for tweet in tweets.iterrows():
            outputs.append(self.get_prediction(tweet[1]))
        return outputs

    def get_prediction(self, tweet: pd.Series, *args):
        good_energy = tweet.topic_clean_energy or tweet.topic_photovoltaics or \
                      tweet.topic_gas or tweet.topic_nuclear
        if tweet.sentiment == 'positive' and good_energy and \
                not tweet.topic_coal:
            return 'for'
        if tweet.sentiment == 'positive' and tweet.topic_coal and \
                not good_energy:
            return 'against'
        if tweet.sentiment == 'negative' and good_energy and not \
                tweet.topic_coal:
            return 'against'
        if tweet.sentiment == 'negative' and tweet.topic_coal and \
                not good_energy:
            return 'for'
        return 'neutral'
