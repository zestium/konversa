# Conversational agent

import time


class ConversationManager:

    user_data = {}

    seconds = time.time()
    local_time = time.ctime(seconds)

    def __init__(self):

        self.user_data["started"] = self.local_time

    def set_user_data(self, key, value):

        self.user_data[key] = value

    def get_user_data(self, key):

        return self.user_data[key]

    def get_all_user_data(self):

        return self.user_data
