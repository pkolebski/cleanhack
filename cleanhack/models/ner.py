from typing import List

import spacy

from cleanhack.models.base import Model

DEFAULT_MODEL = 'en_core_web_lg'


class NamedEntityRecognizer(Model):
    def __init__(self):
        self.nlp = spacy.load(DEFAULT_MODEL, disable=['tagger', 'parser'])

    def get_prediction(self, tweet_doc):
        locations = self._extract_ent(tweet_doc, 'GPE')
        organisations = self._extract_ent(tweet_doc, 'ORG')
        return locations, organisations

    def predict(self, texts: List[str]):
        ents = []
        for doc in self.nlp.pipe(texts):
            ents.append(self.get_prediction(doc))
        return zip(*ents)

    def _extract_ent(self, doc, target_label):
        return [ent.text for ent in doc.ents if ent.label_ == target_label]


if __name__ == '__main__':
    example_tweets = ["There was an event in New York. Fortum Clean Energy provides energy."]
    model = NamedEntityRecognizer()
    extracted_metadata = model.get_prediction(example_tweets)
    print(extracted_metadata)
