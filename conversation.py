import json
import os
from watson_developer_cloud import ConversationV1



class Conversation:

    def __init__(self, username):
        self.username = username
        self.context = {}
        self.context['user_name'] = self.username
        self.conversation = ConversationV1(password='GBvL0jyr2BzP', username='d6cafd45-923f-4f68-9bea-65a1167973ff', version='2017-05-26')

    def convo(self, text=None):

        intent = None
        output = None
        user_input = text
        response = self.conversation.message(
            workspace_id='e380de5b-7f5b-4287-beb4-3843f449de30',
            input={
                'text': user_input
            },
            context=self.context,

        )

        # If an intent was detected, print it to the console.
        if response['intents']:
            intent = response['intents'][0]['intent']

        if response['output']['text']:
            output = response['output']['text'][0]

        else:
            return "damn! some error occurred!"

        self.context = response['context']
        return intent, output

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
        intent, output = test.convo(input())
        print(intent + '\n' + output)
