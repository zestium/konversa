# Conversation Processor

import redis

from .helpers.cp.sparql.who import *
from .helpers.cp.goal.meeting.reserve import *
from .nlg import *

r = redis.Redis()

class ConversationProcessor:

    def __init__(self):
        pass

    def reserve_meeting_respond(self, order):

        answer_reserve = NaturalLanguageGeneration('reserve_meeting_' + order, {})

        return answer_reserve.view()

    def answer_who(self, person_data):

        the_answer = AnswerWho(person_data['person_name'])

        ans = {}

        ans['person_name'] = person_data['person_name']
        ans['item_description'] = the_answer.get_item_description()

        populate_answer = NaturalLanguageGeneration('answer_who', ans)

        return populate_answer.view()

