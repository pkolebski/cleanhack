import re
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
                'topic_energy': ['energy', 'fuel', 'power'],
                'topic_clean_energy': ['wind', 'biomass', 'eco-friendly', 'ecology',
                                       'clean', 'renewable', 'green', 'water', 'renewables',
                                       'hydroelectric', 'hydro', 'eco'],
                "topic_photovoltaics": ["photovoltaic", "solar", "sun"],
                'topic_gas': ['gas', 'propane', 'butane'],
                'topic_nuclear': ['nuclear', 'atom'],
                'topic_coal': ['coal', 'mine', 'miner', 'charcoal', 'coalmine'],
            }

    def get_prediction(self, text: str, normalize: bool = True, threshold: float = 0.3):
        scores = dict.fromkeys(self.keywords, 0)
        text = re.sub(r"[^A-Za-z\'\-]+", " ", text)
        text = set([self.model.lemmatize(w) for w in text.split()])
        for k, keywords in self.keywords.items():
            for word in keywords:
                if word in text:
                    scores[k] += 1

        if (v_sum := sum(scores.values())) > 0 and normalize:
            scores = {k: 1 if v / v_sum >= threshold else 0 for k, v in scores.items()}
            scores['other'] = 0
        else:
            scores = dict.fromkeys(self.keywords, 0)
            scores['other'] = 1
        return scores


if __name__ == '__main__':
    model = Topics()
    print(model.predict([
        "COVID doesn't exist!!!11",
        "I hate coal mines, I will have eco-friendly photovoltaic panels "
        "on my ecology house"
    ]))
