from __future__ import unicode_literals, print_function

from datetime import datetime
import plac
import random
from pathlib import Path
import spacy
from tqdm import tqdm

data = open("data/trainining_data.txt", "r").read()
data = eval(data)

iter_and_loss = list()
# new entity label
LABEL = set()

# Training data
TRAIN_DATA = list()
for td in data:
    if td[1]['entities']:
        TRAIN_DATA.append(td)
        LABEL.add(td[1]['entities'][0][2])


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    new_model_name=("New model name for model meta.", "option", "nm", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_iter=("Number of training iterations", "option", "n", int))


def main(model=None, new_model_name='CUSTOM MODEL', output_dir='trained model', n_iter=700):
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
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in tqdm(TRAIN_DATA):
                nlp.update([text], [annotations], sgd=optimizer, drop=0.35,
                           losses=losses)
            iter_and_loss.append({'Iteration':itn+1, 'Loss':losses})
            print(f'Iteration:{itn + 1}   Loss:{losses}')

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

        # Save history
        history = open(f"{output_dir}/{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} model history.txt", "w")
        history.write(str(iter_and_loss))
        history.close()

        print("Saved model and history to", output_dir)

if __name__ == '__main__':
    plac.call(main)