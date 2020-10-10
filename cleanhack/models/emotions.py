from transformers import AutoModelWithLMHead, AutoTokenizer

from cleanhack.models.base import Model


class Emotions(Model):
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("mrm8488/t5-base-finetuned-emotion")
        self.model = AutoModelWithLMHead.from_pretrained("mrm8488/t5-base-finetuned-emotion")

    def get_prediction(self, text: str):
        input_ids = self.tokenizer.encode(text + '</s>', return_tensors='pt')
        output = self.model.generate(input_ids=input_ids, max_length=2)

        dec = [self.tokenizer.decode(ids) for ids in output]
        return dec[0]


if __name__ == "__main__":
    model = Emotions()
    preds = model.predict([
        "i am sad",
        "i have a feeling i kinda lost my best friend"
    ])
    print(preds)
