from __future__ import unicode_literals, print_function
import spacy

test_text = '''

Mobile TopUp Limited is backed by a Singapore VC and software company specialized in fintech, blockchain and cross border money transfer.
Key expertise in the mobile wallet and international cross border payment.
Position: Backend software engineer
------
Key responsibilities:
Requirement analysis
System design
Documentation
Development
Client meeting (English)
-------
We expect you have:
Solid knowledge of Laravel, PHP
Node, Javascript, React
AWS, RDS, Load balancer, etc
Git, Jira, etc
-------
Office: Mirpur DOHS
Work from home: Yes (Until further notice)
-------
Salary range: 50K-80k
Joining: As soon as possible
-------
Office facility:
Decorated Office
Mac book
5 days office
Office lunch
Tea-Coffe-Snacks

Apply here
https://forms.gle/Q14FX5MMgstqZDbp6

'''
load_model = 'trained model/'

# test the saved model
nlp = spacy.load(load_model)
doc = nlp(test_text)
for ent in doc.ents:
    print(f'{ent.label_} is {ent.text}')