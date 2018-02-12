from conversation import Conversation
from knowledge import Knowledge
from speech import Speech
from vision import Vision
from my_nlg import NLG
from perfromers import Performers
from holidays import Holidays
from dictionary import Dictionary
import requests
import json
import datetime
import dateutil
import sys
from tp import Twilio
sys.path.append("./")

user_name = 'vinay'
launch_phrase = "ok"
use_launch_phrase = True
debugger_enabled = True
camera = 0
weather_api_token = 'd35c29eecae9b60ada2a0565f75ec5b9'
twilio_account_sid = "AC54ae2752e1452a934167476156168571"
twilio_auth_token = "7264a522752fc9da26cee19bc7eb066d"

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
        self.twilio = Twilio(twilio_account_sid, twilio_auth_token)

    def start(self):
        """
        Main loop. Waits for the launch phrase, then decides an action.
        :return:
        """
        test = False

        requests.get("http://localhost:8080/clear")
        if self.vision.recognize_face():
            requests.get("http://localhost:8080/statement?text=Found Face")
            requests.get("http://localhost:8080/clear")

            if use_launch_phrase:
                while True:
                    recognizer, audio = self.speech.listen_to_voice()
                    if self.speech.is_call_to_action(recognizer, audio):
                        self.__acknowledge_action()
                        break

        while True:
            try:
                self.decide_action()
            except ValueError:
                self.__text_action('I am sorry! some problem has occured. would you mind asking me some another query?')
            except requests.exceptions.HTTPError:
                self.__text_action('I am sorry! some problem has occured. would you mind asking me some another query?')

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
                    requests.get("http://localhost:8080/clear")
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
                    self.__text_action(format)

                    if count > 2:
                        format = f"and we also have a holiday at {data[2]},  on the occasion of {data[3]}"
                        self.__text_action(format)

                elif intent == 'dictionary':

                    if entities == 'dict_values' and value1 == 'definition' or value2 == 'definition':

                        word = self.conversation_obj.response['context']['word']
                        output = self.dictionary.defination(word)
                        print(output)
                        self.__text_action(output)

                    if entities == 'dict_values' and value1 == 'antonym' or value2 == 'antonym':
                        word = self.conversation_obj.response['context']['word']
                        output = self.dictionary.antonyms(word)
                        print(output)
                        self.__text_action(output)

                    if entities == 'dict_values' and value1 == 'synonym' or value2 == 'synonym':
                        word = self.conversation_obj.response['context']['word']
                        output = self.dictionary.synonyms(word)
                        print(output)
                        self.__text_action(output)

                    if entities == 'dict_values' and value1 == 'rhyme' or value2 == 'rhyme':
                        word = self.conversation_obj.response['context']['word']
                        output = self.dictionary.rhymes(word)
                        print(output)
                        self.__text_action(output)

                elif intent == 'send_sms':
                    self.__text_action(output)
                    person = self.conversation_obj.response['context']['person']
                    recognizer, audio = self.speech.listen_to_voice()
                    speech = self.speech.google_speech_recognition(recognizer, audio)
                    intent, entities, value1, value2, output = self.conversation_obj.convo(speech)

                    message = self.conversation_obj.response['context']['message']
                    to = self.twilio.phone_log[person]
                    self.twilio.send_sms(to.lower(), message)
                    self.__text_action(output)







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

                elif intent == 'weather':
                    self.__text_action(output)
                    self.__weather_action()

                else:
                    self.__text_action(output)
            except Exception as e:
                print('failed')
                print(e)
                self.__text_action("I'm sorry, I couldn't understand what you meant by that")
                return

            self.decide_action()

    def __text_action(self, text=None):
        if text is not None:
            requests.get("http://localhost:8080/statement?text=%s" % text)
            self.speech.synthesize_text(text)

    def __acknowledge_action(self):
        self.__text_action(self.nlg.acknowledge())

    def __news_action(self):
        headlines = self.knowledge.get_news()

        if headlines:
            requests.post("http://localhost:8080/news", data=json.dumps({"articles": headlines}))
            interest = self.nlg.article_interest(headlines)
            if interest is not None:
                self.speech.synthesize_text(interest)
        else:
            self.__text_action("I had some trouble finding news for you")

    def __news(self):
        data = (self.knowledge.get_news())
        requests.post("http://localhost:8080/news", data=json.dumps({"articles": data}))
        for i in data:
            print(i)
        for i in data:
            self.speech.synthesize_text(i)



if __name__ == "__main__":
    bot = Bot()
    bot.start()