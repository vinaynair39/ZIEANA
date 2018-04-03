import requests
import json


class Dictionary:

    def __init__(self):
        self.headers = {
            "X-Mashape-Key": "u2eXSrtP7VmshQZCxVeARui9MZqbp1ANN4XjsnaTGjmy2oiSB6",
            "Accept": "application/json"
        }
        self.define = None
        self.anto = None
        self.syno = None
        self.rhyme = None

    def defination(self, word):
        response = requests.get("https://wordsapiv1.p.mashape.com/words/{}".format(word), headers=self.headers)
        resp_json = json.loads(response.text)
        try:
            self.define = resp_json['results'][0]['definition']
        except Exception:
            pass
        if self.define is None:
            return 'oh damn! I could not find any proper definition for the word {};  I am sorry, maybe I could find you some other things?'.format(word)
        else:
            return 'The defination of the word {}, is "{}"'.format(word, self.define)

    def synonyms(self, word):
        response = requests.get("https://wordsapiv1.p.mashape.com/words/{}".format(word), headers=self.headers)
        resp_json = json.loads(response.text)
        try:
            self.syno = resp_json['results'][0]['synonyms'][0]
        except Exception:
            pass
        if self.syno is None:
            return 'oh damn! I could not find any synonym for the word {};  I am sorry, maybe I could find you some other things?'.format(word)
        else:
            return 'The synonym of {} is, "{}"'.format(word, self.syno)

    def antonyms(self, word):
        response = requests.get("https://wordsapiv1.p.mashape.com/words/{}/antonyms".format(word), headers=self.headers)
        resp_json = json.loads(response.text)
        try:
            self.anto = resp_json['antonyms'][0]
        except Exception:
            pass
        if self.anto is None:
            return 'oh damn! I could not find any antonym for the word {};  I am sorry, maybe try some other words?'.format(word)
        else:
            return 'The opposite of {} is, "{}"'.format(word, self.anto)

    def rhymes(self, word):
        response = requests.get("https://wordsapiv1.p.mashape.com/words/{}/rhymes".format(word), headers=self.headers)
        resp_json = json.loads(response.text)
        try:
            self.rhyme = resp_json['rhymes']['all'][0]
            if self.rhyme == word:
                self.rhyme = resp_json['rhymes']['all'][1]
        except Exception:
            pass
        if self.rhyme is None:
            return 'oh damn! I could not find any rhyming word for {};  I am sorry, maybe I could find you some other things?'.format(word)
        else:
            return 'I think {} rhymes with, "{}"'.format(word, self.rhyme)


if __name__ == "__main__":
    t = Dictionary()
    data = t.synonyms(input("enter the word"))
    print(data)







