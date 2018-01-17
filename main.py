from conversation import Conversation
from knowledge import Knowledge
from speech import Speech
from vision import Vision
from my_nlg import NLG


user_name = 'vinay'
launch_phrase = "ok"
use_launch_phrase = True
debugger_enabled = False
camera = 0
weather_api_token = 'd35c29eecae9b60ada2a0565f75ec5b9'

class Bot(object):
    def __init__(self):
        self.conversation_obj = Conversation(user_name)
        self.speech = Speech('a40fb4ee-2f84-47ab-acce-c2828b277b08',
                             '1jQFSMbVBjiX',
                             launch_phrase=launch_phrase,
                             debugger_enabled=debugger_enabled
                             )
        self.knowledge = Knowledge(weather_api_token)
        self.vision = Vision(camera=camera)
        self.nlg = NLG()


    def start(self):
        """
        Main loop. Waits for the launch phrase, then decides an action.
        :return:
        """
        # requests.get("http://localhost:8080/clear")
        if self.vision.recognize_face():
            print("Found face")
            if use_launch_phrase:
                recognizer, audio = self.speech.listen_to_voice()
                if self.speech.is_call_to_action(recognizer, audio):
                    self.__acknowledge_action()
                    test = True
            else:
                self.decide_action()

        while test:
            try:
                self.decide_action()
            except ValueError:
                print('I am sorry! some problem has occured. would you mind asking me some another query?')
                self.speech.synthesize_text(
                    'I am sorry! some problem has occured. would you mind asking me some another query?')

            except requests.exceptions.HTTPError:
                print('I am sorry! some problem has occured. would you mind asking me some another query?')
                self.speech.synthesize_text(
                    'I am sorry! some problem has occured. would you mind asking me some another query?')

    def decide_action(self):
        """
        Recursively decides an action based on the intent.
        :return:
        """
        recognizer, audio = self.speech.listen_to_voice()

        # received audio data, now we'll recognize it using Google Speech Recognition
        speech = self.speech.google_speech_recognition(recognizer, audio)

        if speech is not None:
            try:

                entities = None
                intent = None
                value1 = None
                value2 = None
                intent, entities, value1, value2, output = self.conversation_obj.convo(speech)
                print(f'Intent:{intent}\nEntities:{entities}\nValue1:{value1}\nValue2:{value2} ' + intent)
                if intent == 'news':

                    self.__text_action(output)
                    data = (self.knowledge.get_news())
                    for i in data:
                        self.speech.synthesize_text(i)
                else:
                    self.speech.synthesize_text(output)
            except Exception as e:
                print('failed')
                print(e)
                self.__text_action("I'm sorry, I couldn't understand what you meant by that")
                return

            self.decide_action()

    def __text_action(self, text=None):
        if text is not None:
            # requests.get("http://localhost:8080/statement?text=%s" % text)
            self.speech.synthesize_text(text)

    def __acknowledge_action(self):
        self.__text_action(self.nlg.acknowledge())

    def __news_action(self):
        headlines = self.knowledge.get_news()

        if headlines:
            # requests.post("http://localhost:8080/news", data=json.dumps({"articles": headlines}))
            interest = self.nlg.article_interest(headlines)
            if interest is not None:
                self.speech.synthesize_text(interest)
        else:
            self.__text_action("I had some trouble finding news for you")

if __name__ == "__main__":
    bot = Bot()
    bot.start()