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
        response = requests.get(f"https://wordsapiv1.p.mashape.com/words/{word}", headers=self.headers)
        resp_json = json.loads(response.text)
        try:
            self.define = resp_json['results'][0]['definition']
        except Exception:
            pass
        if self.define is None:
            return f'oh damn! I could not find any proper definition for the word {word};  I am sorry, maybe I could find you some other things?'
        else:
            return f'The defination of the word {word}, is "{self.define}"'

    def synonyms(self, word):
        response = requests.get(f"https://wordsapiv1.p.mashape.com/words/{word}", headers=self.headers)
        resp_json = json.loads(response.text)
        try:
            self.syno = resp_json['results'][0]['synonyms'][0]
        except Exception:
            pass
        if self.syno is None:
            return f'oh damn! I could not find any synonym for the word {word};  I am sorry, maybe I could find you some other things?'
        else:
            return f'The synonym of {word} is, "{self.syno}"'

    def antonyms(self, word):
        response = requests.get(f"https://wordsapiv1.p.mashape.com/words/{word}/antonyms", headers=self.headers)
        resp_json = json.loads(response.text)
        try:
            self.anto = resp_json['antonyms'][0]
        except Exception:
            pass
        if self.anto is None:
            return f'oh damn! I could not find any antonym for the word {word};  I am sorry, maybe try some other words?'
        else:
            return f'The opposite of {word} is, "{self.anto}"'

    def rhymes(self, word):
        response = requests.get(f"https://wordsapiv1.p.mashape.com/words/{word}/rhymes", headers=self.headers)
        resp_json = json.loads(response.text)
        try:
            self.rhyme = resp_json['rhymes']['all'][0]
            if self.rhyme == word:
                self.rhyme = resp_json['rhymes']['all'][1]
        except Exception:
            pass
        if self.rhyme is None:
            return f'oh damn! I could not find any rhyming word for {word};  I am sorry, maybe I could find you some other things?'
        else:
            return f'I think {word} rhymes with, "{self.rhyme}"'


if __name__ == "__main__":
    t = Dictionary()
    data = t.synonyms(input("enter the word"))
    print(data)







