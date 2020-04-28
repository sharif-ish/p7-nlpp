from __future__ import unicode_literals, print_function
import spacy

test_text = '''

3DEVs IT Ltd. is looking for Software Engineer (Backend) with a minimum of 2 years experience in Python, Django and Node.js

Company Type: FinTech

Office Hours: 9:00 AM – 6:00 PM (Sun-Thursday)

Office Location: Nasir Trade Center, 89 Bir Uttam CR Datta Road Bangla Motor, Dhaka

Job Category: Developer

Job Type: Full Time

Experience Requirements: Minimum 2 years

Salary Range: BDT 30,000 – 45,000 (Based on experience and skill)

Deadline: 30th April 2020

To know more details about the position and apply process please click the link below

bit.ly/SEBE020420

'''
load_model = 'trained model/'

# test the saved model
nlp = spacy.load(load_model)
doc = nlp(test_text)
for ent in doc.ents:
    print(f'{ent.label_} is {ent.text}')