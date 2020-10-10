import spacy

model_name = 'en_core_web_lg'


def get_entities_from_text(tweets, nlp=None):
    if nlp is None:
        nlp = spacy.load(model_name, disable=['tagger', 'parser'])

    extracted = {'locations': [], 'organisations': []}
    for tweet_doc in nlp.pipe(tweets):
        extracted['locations'].append(_extract_ent(tweet_doc, 'GPE'))
        extracted['organisations'].append(_extract_ent(tweet_doc, 'LOC'))
    return extracted


def _extract_ent(doc, target_label):
    return [ent.text for ent in doc.ents if ent.label_ == target_label]


if __name__ == '__main__':
    example_tweets = ["There was an event in New York. Fortum Clean Energy provides energy."]
    extracted_metadata = get_entities_from_text(example_tweets)
    print(extracted_metadata)
