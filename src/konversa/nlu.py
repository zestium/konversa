# Natural Language Understanding module

import spacy

nlp = spacy.load("en_core_web_lg")


class IntentEngine:

    def __init__(self, the_text):
        self.doc = nlp(the_text)

    def add_str(self):
        return self.doc + 'uhui'

    def get_ner(self):

        returned_str = ''

        for ent in self.doc.ents:
            returned_str += ent.text
            returned_str += ' - ' + ent.text
            returned_str += ' - ' + ent.label_
            returned_str += ' - ' + str(spacy.explain(ent.label_))

        return returned_str
