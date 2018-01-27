import json
import os
from watson_developer_cloud import ConversationV1



class Conversation:

    def __init__(self, username):
        self.username = username
        self.context = {}
        self.response = None
        self.word = None
        self.context['user_name'] = self.username
        self.conversation = ConversationV1(password='GBvL0jyr2BzP', username='d6cafd45-923f-4f68-9bea-65a1167973ff', version='2017-05-26')
        self.intent = None
        self.entities = None
        self.value1 = None
        self.value2 = None
        self.output = None

    def convo(self, text=None):

        user_input = text
        self.response = self.conversation.message(
            workspace_id='e380de5b-7f5b-4287-beb4-3843f449de30',
            input={
                'text': user_input
            },
            context=self.context,

        )
        print(self.response)
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
            self.value2 = self.response['entities'][0]['value']
        except Exception:
            pass

        self.context = self.response['context']
        return self.intent, self.entities, self.value1, self.value2, self.output

    def convoV2(self, user_name):

        context = {}
        context['user_name'] = user_name
        conversation = ConversationV1(password=self.password, username=self.username, version='2017-05-26')
        while True:
            user_input = input('>> ')
            response = conversation.message(
                workspace_id='e380de5b-7f5b-4287-beb4-3843f449de30',
                input={
                    'text': user_input
                },
                context=context,

            )

            # If an intent was detected, print it to the console.
            if response['intents']:
                print('Detected intent: #' + response['intents'][0]['intent'])

            if response['output']['text']:
                print(response['output']['text'][0])

            else:
                return "damn! some error occurred!"

            context = response['context']

if __name__ == '__main__':
    test = Conversation('vinay')
    while True:
        intent, entities, value1, value2, output = test.convo(input())
        test.word = test.response['context']['word']
        print(intent)
        print(entities)
        print(value1)
        print(value2)
        print(test.word)