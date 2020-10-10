from abc import abstractmethod
from typing import List


class Model:
    @abstractmethod
    def get_prediction(self, text: str):
        pass

    def predict(self, texts: List[str]):
        outputs = []
        for text in texts:
            outputs.append(self.get_prediction(text))
        return outputs
