from __future__ import unicode_literals, print_function
import spacy

test_text = 'We (Softwind Tech) are LOOKING for experienced Data Scientist'
load_model = 'trained model/'

# test the saved model
nlp = spacy.load(load_model)
doc = nlp(test_text)
for ent in doc.ents:
    print(f'{ent.label_} is {ent.text}')