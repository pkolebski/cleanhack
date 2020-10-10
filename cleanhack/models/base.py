from abc import abstractmethod
from typing import List


class Model:
    def __call__(self, *args, **kwargs):
        return self.predict(*args, **kwargs)

    @abstractmethod
    def get_prediction(self, text: str, *args, **kwargs):
        pass

    def predict(self, texts: List[str], *args, **kwargs):
        outputs = []
        for text in texts:
            outputs.append(self.get_prediction(text, *args, **kwargs))
        return outputs
