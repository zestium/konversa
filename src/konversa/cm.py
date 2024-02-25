# Conversation Management

import time


class ConversationManager:

    user_data = {}

    seconds = time.time()
    local_time = time.ctime(seconds)
    in_conversation = False

    def __init__(self):

        self.user_data["started"] = self.local_time

    def set_user_data(self, key, value):

        self.user_data[key] = value

    def get_user_data(self, key):

        return self.user_data[key]

    def get_all_user_data(self):

        return self.user_data

    def set_in_conversation(self, value):

        self.in_conversation = value

    def get_in_conversation(self):

        return self.in_conversation

