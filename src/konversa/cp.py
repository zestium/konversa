# Conversation Processor

import redis
r = redis.Redis()

class ConversationProcessor:

    list_of_steps = []

    def __init__(self, intent):

        self.reply = r.graph(intent).query("MATCH (n) RETURN n")

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


