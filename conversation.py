import json
import os
from watson_developer_cloud import ConversationV1



class Conversation:

    def __init__(self):
        self.context = {}
        self.response = None
        self.word = None
        self.context['user_name'] = ''
        self.conversation = ConversationV1(password='GBvL0jyr2BzP', username='d6cafd45-923f-4f68-9bea-65a1167973ff', version='2018-02-16')
        self.intent = None
        self.entities = None
        self.value1 = ""
        self.value2 = ""
        self.output = None

    def set_user_name(self, username):
        self.context['user_name'] = username

    def convo(self, text=None):

        user_input = text

        self.response = self.conversation.message(
            workspace_id='e380de5b-7f5b-4287-beb4-3843f449de30',
            input={
                'text': user_input
            },
            context=self.context,

        )
        # If an intent was detected, print it to the console.
        if self.response['intents']:
            self.intent = self.response['intents'][0]['intent']
        else:
            self.intent = None

        if self.response['output']['text']:
            self.output = self.response['output']['text'][0]
        else:
            self.output = None

        try:
            self.entities = self.response['entities'][0]['entity']
        except Exception:
            pass

        try:
            self.value1 = self.response['entities'][0]['value']
        except Exception:
            pass

        try:
            self.value2 = self.response['entities'][1]['value']
        except Exception:
            pass

        if self.value2 is None:
            self.value2 = ""

        self.context = self.response['context']
        return self.intent, self.entities, self.value1, self.value2, self.output

if __name__ == '__main__':
    test = Conversation()
    while True:
        intent, entities, value1, value2, output = test.convo(input("go:"))
        print('1 ' + intent)

