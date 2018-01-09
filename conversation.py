import json
import os
from watson_developer_cloud import ConversationV1



class Conversation:


    username = 'd6cafd45-923f-4f68-9bea-65a1167973ff'
    password = 'GBvL0jyr2BzP'

    def convo(self, text=None):
        conversation = ConversationV1(password=self.password, username=self.username, version='2017-05-26')

        response = conversation.message(
            workspace_id='e380de5b-7f5b-4287-beb4-3843f449de30',
            input={
                'text': text
            },
            context={'user_name': 'vinay'}
        )
        # intent = response['intents'][0]['intent']
        resp_text = response['output']['text'][0]
        return resp_text, response

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
    test = Conversation()
    test.convoV2('david')
