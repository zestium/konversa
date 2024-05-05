# Conversation Processor

import redis

from .helpers.cp.sparql.who import *
from .nlg import *

r = redis.Redis()

class ConversationProcessor:

    list_of_steps = []

    def __init__(self, intent, data_from_message):

        self.reply = r.graph(intent).query("MATCH (n) RETURN n")
        self.the_data_from_message = data_from_message['person_name']

    def get_steps(self):

        for a in self.reply.result_set:
            for x in a:
                self.list_of_steps.append(x.label)

        return self.list_of_steps

    def get_number_of_steps(self):

        nos = 0

        for a in self.reply.result_set:
            for x in a:
                if x.label == "Begin":
                    nos = x.properties["num_of_steps"]

        return nos

    def answer_who(self):

        the_answer = AnswerWho(self.the_data_from_message)

        ans = {}

        ans['person_name'] = self.the_data_from_message
        ans['item_description'] = the_answer.get_item_description()

        populate_answer = NaturalLanguageGeneration('answer_who', ans)

        return populate_answer.view()

