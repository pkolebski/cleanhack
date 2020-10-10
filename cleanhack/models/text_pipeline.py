from typing import List

import pandas as pd

from cleanhack.models.base import Model
from cleanhack.models.emotions import Emotions
from cleanhack.models.ner import NamedEntityRecognizer
from cleanhack.models.sentiment import Sentiment


class TextPipeline(Model):
    EMOTIONS_MAPPING = {'anger', 'joy'}

    def __init__(self, ner=None, emotions=None, sentiment=None):
        self.ner = NamedEntityRecognizer() if ner is None else ner
        self.emotions = Emotions() if emotions is None else emotions
        self.sentiment = Sentiment() if sentiment is None else sentiment

    def get_prediction(self, texts: List[str]):
        locations, organisations = self.ner(texts)
        sentiment = [sent[0]['label'].lower() for sent in self.sentiment(texts)]
        emotion = self.emotions(texts)
        return {
            'mentioned_locations': list(locations),
            'mentioned_organizations': list(organisations),
            'sentiment': sentiment,
            'emotion': emotion
        }

    def predict(self, texts: List[str]):
        return pd.DataFrame(self.get_prediction(texts))


if __name__ == '__main__':
    pipeline_model = TextPipeline()
    tweets = [
        "Yesterday it was raining in New York",
        "Gazeta Wroclawska is the best newspaper"
    ]
    pipeline_result = pipeline_model.predict(tweets)
    print(pipeline_result)
