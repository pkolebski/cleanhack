import re
from collections import defaultdict
from typing import Dict, List

import nltk
from nltk.stem import WordNetLemmatizer

from cleanhack.models.base import Model


class Topics(Model):
    def __init__(self, keywords: Dict[str, List[str]] = None):
        nltk.download('wordnet')
        self.model = WordNetLemmatizer()
        if keywords is not None:
            self.keywords = keywords
        else:
            self.keywords = {
                'energy': ['energy', 'fuel', 'power'],
                'clean energy': ['photovoltaic', 'wind', 'biomass', 'eco-friendly', 'ecology',
                                 'clean', 'solar', 'renewable', 'green', 'water', 'renewables',
                                 'hydroelectric', 'eco'],
                'gas': ['gas', 'propane', 'butane'],
                'nuclear': ['nuclear', 'atom'],
                'coal': ['coal', 'mine', 'miner', 'charcoal', 'coalmine'],
            }

    def get_prediction(self, text: str, normalize: bool = True):
        scores = defaultdict(int)
        text = re.sub(r"[^A-Za-z\'\-]+", " ", text)
        text = set([self.model.lemmatize(w) for w in text.split()])
        for k, keywords in self.keywords.items():
            for word in keywords:
                if word in text:
                    scores[k] += 1

        if (v_sum := sum(scores.values())) > 0 and normalize:
            scores = {k: v / v_sum for k, v in scores.items()}
        return scores


if __name__ == '__main__':
    model = Topics()
    print(model.predict([
        "COVID doesn't exist!!!11",
        "I hate coal mines, I will have eco-friendly photovoltaic panels "
        "on my ecology house"
    ]))
