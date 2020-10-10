import pandas as pd

from cleanhack.models.base import Model


class Stance(Model):
    def get_prediction(self, tweet: pd.DataFrame):
        good_energy = tweet.topic_clean_energy or tweet.topic_photovoltaics or \
                      tweet.topic_gas or tweet.topic_nuclear
        if tweet.sentiment == 'positive' and good_energy and \
                not tweet.topic_coal:
            return 1
        if tweet.sentiment == 'positive' and tweet.topic_coal and \
                not good_energy:
            return -1
        if tweet.sentiment == 'negative' and good_energy and not \
                tweet.topic_coal:
            return -1
        if tweet.sentiment == 'negative' and tweet.topic_coal and \
                not good_energy:
            return 1
        return 0
