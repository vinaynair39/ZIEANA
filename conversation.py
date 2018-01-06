import json
import os
from watson_developer_cloud import ConversationV1



class Conversation:


    username = 'd6cafd45-923f-4f68-9bea-65a1167973ff'
    password = 'GBvL0jyr2BzP'

    def convo(self, text):
        conversation = ConversationV1(password=self.password, username=self.username, version='2017-05-26')

        response = conversation.message(
            workspace_id='e380de5b-7f5b-4287-beb4-3843f449de30',
            input={
                'text': text
            })

        intent = response['intents'][0]['intent']
        resp_text = response['output']['text'][0]
        print(intent)
        data = json.dumps(response, indent=2)
        print(data)
        return intent, resp_text, response
        # data = json.dumps(response, indent=2)
        # # print(data)

    def convoV2(self, text, response):
        data =response['context']
        conversation = ConversationV1(password=self.password, username=self.username, version='2017-05-26')

        response = conversation.message(
            workspace_id='e380de5b-7f5b-4287-beb4-3843f449de30',
            input={
                'text': text
            },
            context=data
        )

        intent = response['intents'][0]['intent']
        resp_text = response['output']['text'][0]
        print(intent)
        data = json.dumps(response, indent=2)
        print(data)
        return intent, resp_text
        # data = json.dumps(response, indent=2)
        # # print(data)



if __name__ == '__main__':
    test = Conversation()
    test.convo('play me some music')

