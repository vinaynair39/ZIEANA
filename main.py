from conversation import Conversation
from knowledge import Knowledge
from speech import Speech
from vision import Vision
from my_nlg import NLG
from perfromers import Performers
from holidays import Holidays
from dictionary import Dictionary

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
        self.nlg = NLG(user_name)
        self.perfromers = Performers()
        self.holidays = Holidays()
        self.dictionary = Dictionary()

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
        speech = self.speech.google_speech_recognition(recognizer, audio)

        if speech is not None:
            try:

                intent, entities, value1, value2, output = self.conversation_obj.convo(speech)

                if intent == 'news':
                    self.__text_action(output)
                    self.__news()


                elif intent == 'current_time':
                    output = 'The time is,  ' + self.knowledge.current_time()
                    self.__text_action(output)

                elif intent == 'current_date':
                    output = 'It\'s,  ' + self.knowledge.current_date()
                    self.__text_action(output)

                elif intent == 'holiday':
                    data = self.holidays.find_next('february')
                    count = len(data)
                    format = f"The next holday is at {data[0]},  on the occasion of {data[1]} "
                    self.speech.synthesize_text(format)

                    if count > 2:
                        format = f"and we also have a holiday at {data[2]},  on the occasion of {data[3]}"
                        self.speech.synthesize_text(format)

                elif intent == 'dictionary':

                    if entities == 'dict_values' and value1 == 'definition' or value2 == 'definition':
                        word = self.conversation_obj.response['context']['word']
                        output = self.dictionary.defination(word)
                        print(output)
                        self.speech.synthesize_text(output)

                    if entities == 'dict_values' and value1 == 'antonym' or value2 == 'antonym':
                        word = self.conversation_obj.response['context']['word']
                        output = self.dictionary.antonyms(word)
                        print(output)
                        self.speech.synthesize_text(output)

                    if entities == 'dict_values' and value1 == 'synonym' or value2 == 'synonym':
                        word = self.conversation_obj.response['context']['word']
                        output = self.dictionary.synonyms(word)
                        print(output)
                        self.speech.synthesize_text(output)

                    if entities == 'dict_values' and value1 == 'rhyme' or value2 == 'rhyme':
                        word = self.conversation_obj.response['context']['word']
                        output = self.dictionary.rhymes(word)
                        print(output)
                        self.speech.synthesize_text(output)





                elif intent == 'music_playlist':
                    self.__text_action(output)
                    recognizer, audio = self.speech.listen_to_voice()
                    speech = self.speech.google_speech_recognition(recognizer, audio)
                    intent, entities, value1, value2, output = self.conversation_obj.convo(speech)
                    self.speech.synthesize_text(output)
                    music_name = self.conversation_obj.response['context']['music_name']
                    print(music_name)
                    self.perfromers.playlist(music_name)

                elif intent == "alarm":
                    self.__text_action(output)
                    recognizer, audio = self.speech.listen_to_voice()
                    speech = self.speech.google_speech_recognition(recognizer, audio)
                    intent, entities, value1, value2, output = self.conversation_obj.convo(speech)
                    self.speech.synthesize_text(output)

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

    def __news(self):
        data = (self.knowledge.get_news())
        for i in data:
            print(i)
        for i in data:
            self.speech.synthesize_text(i)


if __name__ == "__main__":
    bot = Bot()
    bot.start()