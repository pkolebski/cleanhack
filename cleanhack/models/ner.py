from typing import List

import spacy

from cleanhack.models.base import Model

DEFAULT_MODEL = 'en_core_web_lg'


class NamedEntityRecognizer(Model):
    def __init__(self):
        self.nlp = spacy.load(DEFAULT_MODEL, disable=['tagger', 'parser'])

    def get_prediction(self, tweets: List[str]):
        extracted = {'locations': [], 'organisations': []}
        for tweet_doc in self.nlp.pipe(tweets):
            extracted['locations'].append(self._extract_ent(tweet_doc, 'GPE'))
            extracted['organisations'].append(self._extract_ent(tweet_doc, 'LOC'))
        return extracted

    def _extract_ent(self, doc, target_label):
        return [ent.text for ent in doc.ents if ent.label_ == target_label]


if __name__ == '__main__':
    example_tweets = ["There was an event in New York. Fortum Clean Energy provides energy."]
    model = NamedEntityRecognizer()
    extracted_metadata = model.get_prediction(example_tweets)
    print(extracted_metadata)
