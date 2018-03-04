from conversation import Conversation
from knowledge import Knowledge
from speech import Speech
from vision import Vision
from performers import Performers
from holidays import Holidays
from dictionary import Dictionary
from country import Countries
from movies import Movie
import threading
import requests
import json
import sys
import re
from random import random
import random
import datetime
from tp import Twilio
sys.path.append("./")

launch_phrase = {'vinay': 'banana apple smoothie', 'chanan': 'speaker geek', 'others':  'hello'}
use_launch_phrase = True
debugger_enabled = True
camera = 0
weather_api_token = 'd35c29eecae9b60ada2a0565f75ec5b9'
twilio_account_sid = "AC54ae2752e1452a934167476156168571"
twilio_auth_token = "7264a522752fc9da26cee19bc7eb066d"
random.seed(datetime.datetime.now())

class Bot(object):
    def __init__(self):
        self.conversation_obj = Conversation()
        self.speech = Speech('a40fb4ee-2f84-47ab-acce-c2828b277b08',
                             '1jQFSMbVBjiX',
                             launch_phrase=launch_phrase,
                             debugger_enabled=debugger_enabled
                             )
        self.knowledge = Knowledge(weather_api_token)
        self.vision = Vision(camera=camera)
        # self.nlg = NLG()
        self.performers = Performers()
        self.holidays = Holidays()
        self.dictionary = Dictionary()
        self.twilio = Twilio(twilio_account_sid, twilio_auth_token)
        self.movie = Movie()
        self.countries = Countries()
        self.user_name = ""

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
                    condition, key = self.speech.is_call_to_action(recognizer, audio)
                    if condition and key != 'others':
                        self.user_name = key
                        self.conversation_obj.set_user_name(self.user_name)
                        self.__acknowledge_action()
                        break
                    elif condition and key == 'others':
                        self.__simple_acknowledge_action()
                        recognizer, audio = self.speech.listen_to_voice()
                        speech = self.speech.google_speech_recognition(recognizer, audio)
                        intent, entities, value1, value2, output = self.conversation_obj.convo(speech)
                        self.__text_action(output)
                        recognizer, audio = self.speech.listen_to_voice()
                        speech = self.speech.google_speech_recognition(recognizer, audio)
                        intent, entities, value1, value2, output = self.conversation_obj.convo(speech)
                        guest_name_full = ''
                        guest_name = ''
                        try:
                            guest_name_full = self.conversation_obj.context['guest_name_full']
                            guest_name = self.conversation_obj['guest_name']
                        except:
                            pass
                        if guest_name_full != '':
                            guest_name_full = guest_name_full.rsplit(' ', 1)[0]
                            print(guest_name_full)
                            self.user_name = guest_name_full
                            self.conversation_obj.set_user_name(self.user_name)
                            self.__text_action(output)
                            break
                        else:
                            self.user_name = guest_name_full
                            self.conversation_obj.set_user_name(self.user_name)
                            self.__text_action(output)
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
                print(value1 + value2)

                if intent == 'news':
                    self.__text_action(output)
                    requests.get("http://localhost:8080/clear")
                    t = threading.Thread(target=self.__news)
                    t.start()


                elif intent == 'current_time':
                    output = 'The time is,  ' + self.knowledge.current_time()
                    self.__text_action(output)

                elif intent == 'current_date':
                    output = 'It\'s,  ' + self.knowledge.current_date()
                    self.__text_action(output)

                elif intent == 'holiday':
                    data = self.holidays.find_next('march')
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


                elif intent == 'images':
                    self.__text_action(output)
                    word = self.conversation_obj.response['context']['image']
                    word = re.sub(r'^\W*\w+\W*', '', word)
                    image1, image2 = self.performers.find_images(word)
                    body = {'url': image1}
                    requests.post("http://localhost:8080/image", data=json.dumps(body))

                elif intent == 'place_call':
                    self.__text_action(output)
                    person = self.conversation_obj.response['context']['person']
                    to = self.twilio.phone_log[person]
                    self.twilio.place_Call(to)

                elif intent == 'movie':

                    if entities == 'movie_stuff' and value1 == 'rating' or value2 == 'rating':
                        movie_name = self.conversation_obj.response['context']['movie_name']
                        movie_name = re.sub(r'^\W*\w+\W*', '', movie_name)
                        try:
                            data = self.movie.rating(movie_name)
                            info = data['data']
                            poster = data['poster']
                            body = {'url': poster}
                            requests.post("http://localhost:8080/image", data=json.dumps(body))
                            self.speech.synthesize_text(info)
                        except Exception:
                            self.__text_action(f"I couldn't find anything named {movie_name}. try again maybe?")

                    if entities == 'movie_stuff' and value1 == 'plot' or value2 == 'plot':
                        movie_name = self.conversation_obj.response['context']['movie_name']
                        movie_name = re.sub(r'^\W*\w+\W*', '', movie_name)
                        try:
                            data = self.movie.plot(movie_name)
                            info = data['data']
                            poster = data['poster']
                            body = {'url': poster}
                            print(info  + poster)
                            requests.post("http://localhost:8080/image", data=json.dumps(body))
                            self.speech.synthesize_text(info)

                        except Exception:
                            self.__text_action(f"I couldn't find anything named {movie_name}. try again maybe?")

                    if entities == 'movie_stuff' and value1 == 'cast' or value2 == 'cast':
                        movie_name = self.conversation_obj.response['context']['movie_name']
                        movie_name = re.sub(r'^\W*\w+\W*', '', movie_name)
                        try:
                            data = self.movie.cast(movie_name)
                            info = data['data']
                            poster = data['poster']
                            body = {'url': poster}
                            requests.post("http://localhost:8080/image", data=json.dumps(body))
                            self.speech.synthesize_text(info)
                        except Exception:
                            self.__text_action(f"I couldn't find anything named {movie_name}.... Try again maybe?")


                    if entities == 'movie_stuff' and value1 == 'genre' or value2 == 'genre':
                        movie_name = self.conversation_obj.response['context']['movie_name']
                        movie_name = re.sub(r'^\W*\w+\W*', '', movie_name)
                        try:
                            data = self.movie.genre(movie_name)
                            info = data['data']
                            poster = data['poster']
                            body = {'url': poster}
                            requests.post("http://localhost:8080/image", data=json.dumps(body))
                            self.speech.synthesize_text(info)
                        except Exception:
                            self.__text_action(f"I couldn't find anything named {movie_name}. try again maybe?")

                    if entities == 'movie_stuff' and value1 == 'brief' or value2 == 'brief':
                        movie_name = self.conversation_obj.response['context']['movie_name']
                        movie_name = re.sub(r'^\W*\w+\W*', '', movie_name)
                        try:
                            data = self.movie.movie(movie_name)
                            info = data['data']
                            poster = data['poster']
                            body = {'url': poster}
                            requests.post("http://localhost:8080/image", data=json.dumps(body))
                            self.speech.synthesize_text(info)
                        except Exception:
                            self.__text_action(f"I couldn't find anything named {movie_name}. try again maybe?")

                elif intent == "distance":

                    origin = self.conversation_obj.response['context']['origin']
                    origin = origin.lstrip('from')
                    origin = origin.rstrip('to')
                    destination = self.conversation_obj.response['context']['destination']
                    destination = destination.lstrip('to')
                    text = self.knowledge.distance(origin, destination)
                    self.__text_action(text)

                elif intent == 'ola':
                    origin = self.conversation_obj.response['context']['origin']
                    origin = origin.lstrip('from')
                    origin = origin.rstrip('to')
                    origin_lat, origin_lng = self.knowledge.lat_lng(origin)
                    destination = self.conversation_obj.response['context']['destination']
                    destination = destination.lstrip('to')
                    destination_lat, destination_lng = self.knowledge.lat_lng(destination)













                elif  intent == "countries":

                    if entities == 'country' and value1 == "population" or value2 == "population":

                        word = self.conversation_obj.response['context']['country_name']
                        output1 = self.countries.population(word)
                        self.__text_action(output1)

                    if entities == 'country' and value1 == "about" or value2 == "about":

                        word = self.conversation_obj.response['context']['country_name']
                        output1 = self.countries.country_info(word)
                        self.__text_action(output1)

                    if entities == 'country' and value1 == "currency" or value2 == "currency":

                        word = self.conversation_obj.response['context']['country_name']
                        output1 = self.countries.currency(word)
                        self.__text_action(output1)

                    if entities == 'country' and value1 == "capital" or value2 == "capital":

                        word = self.conversation_obj.response['context']['country_name']
                        output1 = self.countries.capital(word)
                        self.__text_action(output1)



                elif intent == "quit_system":
                    self.__text_action("okay! I will be here if you need me.")
                    sys.exit(1)








                elif intent == 'music_playlist':

                    self.__text_action(output)
                    recognizer, audio = self.speech.listen_to_voice()
                    speech = self.speech.google_speech_recognition(recognizer, audio)
                    intent, entities, value1, value2, output = self.conversation_obj.convo(speech)

                    if entities == "something" and value1 == "something" or value2 == "something":
                        self.__text_action(output)
                        music_name = self.performers.random_play()
                        self.performers.play(music_name)
                        requests.get("http://localhost:8080/music")


                    else:

                        self.speech.synthesize_text(output)
                        music_name = self.conversation_obj.response['context']['music_name']
                        print(music_name)
                        if self.performers.playlist(music_name):
                            self.performers.play(music_name)
                            requests.get("http://localhost:8080/music")
                        else:
                            self.__text_action(f"It looks like you don't have {music_name} in your playlist! Shall i play you an other song?")

                elif intent == "direct_music":
                    self.__text_action(output)
                    music_name = self.performers.random_play()
                    self.performers.play(music_name)
                    requests.get("http://localhost:8080/music")




                elif intent == 'turn_off':
                    self.performers.stop()
                    requests.get("http://localhost:8080/clear")




                elif intent == 'weather':
                    self.__text_action(output)
                    self.__weather_action()

                elif intent == 'face':
                    requests.get("http://localhost:8080/face")


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
        self.__text_action(self.acknowledge())

    def __simple_acknowledge_action(self):
        self.__text_action(self.simple_acknowledge())


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

    def time_of_day(self, date, with_adjective=False):
        ret_phrase = ""
        if date.hour < 10:
            ret_phrase = "morning"
            if with_adjective:
                ret_phrase = "%s %s" % ("this", ret_phrase)
        elif (date.hour >= 10) and (date.hour < 18):
            ret_phrase = "afternoon"
            if with_adjective:
                ret_phrase = "%s %s" % ("this", ret_phrase)
        elif date.hour >= 18:
            ret_phrase = "evening"
            if with_adjective:
                ret_phrase = "%s %s" % ("this", ret_phrase)

        return ret_phrase

    def acknowledge(self):

        user_name = self.user_name
        if user_name is None:
            user_name = ""

        simple_acknoledgement = [
            "Hello, do I Know you?",
            "Hello, who is this?"
            "How can I help?"
        ]

        date = datetime.datetime.now()
        time_acknowledgement = [
            f"Good {self.time_of_day(date)}. What can I do for you?",
            f"Hey {user_name}, what's up?",
            f"Good {self.time_of_day(date)} {user_name}. How may I help? ",
        ]

        personal_acknowledgement = [
            "What can I do for you, %s" % user_name,
            "Hi %s, what can I do for you?" % user_name,
            "Hey %s, what can I do for you?" % user_name
        ]



        ret_phrase = ""
        choice = 0
        if user_name is not None:
            choice = random.randint(1, 2)   # gives   1 or 2

        ret_phrase = ""

        if choice == 1:
            ret_phrase = random.choice(time_acknowledgement)
        else:
            ret_phrase = random.choice(personal_acknowledgement)

        return ret_phrase


    def simple_acknowledge(self):
        simple_acknoledgement = [
            "Hello, do I Know you?",
        ]
        ret_phrase = random.choice(simple_acknoledgement)
        return ret_phrase

    def dictionary_nlg(self):

        phrases = [
            "Alright!",
            "sure, Let me think!",
            "ay ay captain!",
            "I'm on it!"
        ]

        return random.choice(phrases)


if __name__ == "__main__":
    bot = Bot()
    bot.start()