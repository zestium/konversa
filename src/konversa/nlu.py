# Natural Language Understanding module

import spacy
from .helpers.nlu.classifier import *

nlp = spacy.load("en_core_web_sm")

class IntentEngine:

    synapse_0 = []
    synapse_1 = []

    def __init__(self, training_file):

        self.tfile = training_file

    def train_intent(self):

        self.intent_classifier = ClassifyIntent(self.tfile)

        X, y = self.intent_classifier.preprocess_training_data()

        self.synapse_0, self.synapse_1 = self.intent_classifier.train(X, y, hidden_neurons=20, alpha=0.1, epochs=100000, dropout=False, dropout_percent=0.2)

    def classify_intent(self, the_text):

        return self.intent_classifier.classify(the_text, self.synapse_0, self.synapse_1)

    def get_ner(self, the_text):

        self.doc = nlp(the_text)

        returned_str = ''

        for ent in self.doc.ents:
            returned_str += ent.text
            returned_str += ' - ' + ent.text
            returned_str += ' - ' + ent.label_
            returned_str += ' - ' + str(spacy.explain(ent.label_))

        return returned_str
