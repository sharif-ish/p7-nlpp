from __future__ import unicode_literals, print_function

import plac
import random
from pathlib import Path
import spacy
from tqdm import tqdm

# new entity label
LABEL = ['JOB TITLE', 'SKILL', 'VACANCY']

train_data = [
    ("Hiring Senior Full Stack Developer",{'entities':[ (7, 34, 'JOB TITLE') ]}),
    ("Company: Studio Seventy1", {'entities':[ ]}),
    ("Company website: https://seventy1.studio/", {'entities':[ ]}),
    ("Starting Salary: 80,000 - 150,000  BDT", {'entities':[ ]}),
    ("Salary review: Every 6 months.", {'entities':[ ]}),
    ("Vacancy: 1",{'entities':[ (9, 10, 'VACANCY') ]}),
    ("Job Type: Full-Time (Remote)", {'entities':[ ]}),
    ("Deadline: 25 April", {'entities':[ ]}),
    ("Working Hours: 7.5 hours per day, 5 days per week.", {'entities':[ ]}),
    ("Must have:", {'entities':[ ]}),
    ("3+ years of solid experience in Web Development", {'entities':[ ]}),
    ("Extensive experience with JavaScript",{'entities':[ (26, 36, 'SKILL') ]}),
    ("Very comfortable working with React/redux or Vue/Vuex",{'entities':[ (30, 35, 'SKILL'), (36, 41, 'SKILL'), (45, 48, 'SKILL'), (49, 53, 'SKILL') ]}),
    ("Experience working with NodeJs, PHP",{'entities':[ (24, 30, 'SKILL'), (32, 35, 'SKILL') ]}),
    ("Experience working with FireBase/MongoDB, MySQL",{'entities':[ (24, 32, 'SKILL'), (33, 40, 'SKILL'), (42, 47, 'SKILL') ]}),
    ("Nice to have:", {'entities':[ ]}),
    ("Experience with AWS",{'entities':[ (16, 19, 'SKILL') ]}),
    ("Unit testing / TDD",{'entities':[ (0, 12, 'SKILL'), (14, 18, 'SKILL') ]}),
    ("WordPress plugin development",{'entities':[ (0, 28, 'SKILL') ]}),
    ("Responsibilities:", {'entities':[ ]}),
    ("Build & design JavaScript & PHP Web Apps",{'entities':[ (15, 25, 'SKILL'), (28, 31, 'SKILL') ]}),
    ("Maintain and support existing Web Apps", {'entities':[ ]}),
    ("Follow best practices & ship code to production everyday", {'entities':[ ]}),
    ("Benefits:", {'entities':[ ]}),
    ("Opportunity to work for foreign clients", {'entities':[ ]}),
    ("Great opportunity for career progress", {'entities':[ ]}),
    ("Weekly two days off", {'entities':[ ]}),
    ("Application Procedure:", {'entities':[ ]}),
    ("Please send CV to contact@seventy1.studio with the subject “Senior  Full Stack Developer”", {'entities':[ ]}),
    ("If you have any questions, comment below. We will answer shortly.", {'entities':[ ]}),
    ("PS: Please share the message and help others to know this opportunity.", {'entities':[ ]}),
    ("Title: Senior iOS Developer Vacancy: 01 Job Context:", {'entities':[(6, 27, 'JOB TITLE')]}),

    ("Hiring Senior Full Stack Developer Company: Studio Seventy1 Company website: https://seventy1.studio/ Starting Salary: 80,000 - 150,000  BDT Salary review: Every 6 months.", {
        'entities': [(7, 34, 'JOB TITLE')]
    }),

    ("Softzino Technologies Uttara, Dhaka 1230 Sr. Software Engineer (Web) (6 Person) � Hands-on experience on Laravel and Advanced PHP (Composer Packages) Must have experience in developing SaaS-based applications Strong skills on Vue or React or Angular JS, a good understanding of MVC and OOP", {
        'entities': [(41, 62, 'JOB TITLE')]
    }),

    ("Circle FinTech Ltd is looking for UI/ UX Designer with minimum 1-2 years of relevant experience.", {
        'entities': [(34, 49, 'JOB TITLE')]
    }),

    ("𝐁𝐫𝐚𝐢𝐧 𝐒𝐭𝐚𝐭𝐢𝐨𝐧 𝟐𝟑 𝐋𝐭𝐝. is looking for Technical Project Manager.", {
        'entities': [(54, 79, 'JOB TITLE')]
    }),

    ("We are hiring Sr. Dot Net Engineer?", {
        'entities': [(18, 34, 'JOB TITLE')]
    }),

    ("We, ITIW are hiring Unity3D Game Developer", {
        'entities': [(28, 42, 'JOB TITLE')]
    }),

    ("TITLE OF POSITION: Data Scientist", {
        'entities': [(19, 33, 'JOB TITLE')]
    }),

    ("Job Openings for Software Engineers in Dhaka, Bangladesh", {
        'entities': [(17, 35, 'JOB TITLE')]
    })
]
@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    new_model_name=("New model name for model meta.", "option", "nm", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))


def main(model=None, new_model_name='CUSTOM MODEL', output_dir='trained model/', n_iter=1000):
    """Set up the pipeline and entity recognizer, and train the new entity."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")
    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe('ner')

    for l in LABEL:
        ner.add_label(l)   # add new entity label to entity recognizer

    if model is None:
        optimizer = nlp.begin_training()
    else:
        # Note that 'begin_training' initializes the models, so it'll zero out
        # existing entity types.
        optimizer = nlp.entity.create_optimizer()

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        for itn in range(n_iter):
            random.shuffle(train_data)
            losses = {}
            for text, annotations in tqdm(train_data):
                nlp.update([text], [annotations], sgd=optimizer, drop=0.35,
                           losses=losses)
            print(losses)

    # test the trained model
    '''
    test_text = 'We (Softwind Tech) are LOOKING for experienced Game Developer'
    doc = nlp(test_text)
    print("Entities in '%s'" % test_text)
    for ent in doc.ents:
        print(ent.label_, ent.text)
    '''
    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta['name'] = new_model_name  # rename model
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

if __name__ == '__main__':
    plac.call(main)