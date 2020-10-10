from abc import abstractmethod
from typing import List

from tqdm.auto import tqdm


class Model:
    def __call__(self, *args, **kwargs):
        return self.predict(*args, **kwargs)

    @abstractmethod
    def get_prediction(self, text: str, *args, **kwargs):
        pass

    def predict(self, texts: List[str], *args, **kwargs):
        outputs = []
        for text in tqdm(texts, desc=type(self).__name__):
            outputs.append(self.get_prediction(text, *args, **kwargs))
        return outputs
