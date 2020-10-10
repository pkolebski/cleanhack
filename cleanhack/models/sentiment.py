from transformers import pipeline

from cleanhack.models.base import Model


class Sentiment(Model):
    def __init__(self):
        self.model = pipeline('sentiment-analysis')

    def get_prediction(self, text: str):
        return self.model(text)


if __name__ == '__main__':
    model = Sentiment()
    print(model.predict(["I think you are ok."]))
