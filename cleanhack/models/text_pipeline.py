from collections import defaultdict
from typing import List

import pandas as pd

from cleanhack.models.base import Model
from cleanhack.models.emotions import Emotions
from cleanhack.models.ner import NamedEntityRecognizer
from cleanhack.models.sentiment import Sentiment
from cleanhack.models.topic import Topics
from cleanhack.settings import PROCESSED_TWITTER_DATA, TWITTER_DATA_PATH


class TextPipeline(Model):
    def __init__(self, ner=None, emotions=None, sentiment=None):
        self.ner = NamedEntityRecognizer() if ner is None else ner
        self.emotions = Emotions() if emotions is None else emotions
        self.sentiment = Sentiment() if sentiment is None else sentiment
        self.topic = Topics()

    def get_prediction(self, texts: List[str], *args, **kwargs):
        topics = self._transform_topics(self.topic(texts))
        locations, organisations = self.ner(texts)
        sentiment = [sent[0]['label'].lower() for sent in self.sentiment(texts)]
        emotion = self.emotions(texts)
        result = {
            'mentioned_locations': list(locations),
            'mentioned_organizations': list(organisations),
            'sentiment': sentiment,
            'emotion': emotion
        }
        result.update(topics)
        return result

    def predict(self, dataset: pd.DataFrame, text_col_name='text', *args, **kwargs):
        texts = dataset[text_col_name]
        model_results = pd.DataFrame(self.get_prediction(texts))
        dataset = dataset.join(model_results)
        return dataset

    @staticmethod
    def _transform_topics(topics):
        topics_extracted = defaultdict(list)
        for tweet_topics in topics:
            for topic, topic_indicator in tweet_topics.items():
                topics_extracted[topic].append(topic_indicator)
        return topics_extracted


if __name__ == '__main__':
    df = pd.read_json(TWITTER_DATA_PATH)
    pipeline_model = TextPipeline()
    pipeline_result = pipeline_model.predict(df)
    print(pipeline_result)
    pipeline_result.to_csv(PROCESSED_TWITTER_DATA)
