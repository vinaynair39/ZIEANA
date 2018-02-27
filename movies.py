import json
import requests
from speech import Speech


class Movie:

    def __init__(self):
        self.key = 'e63c785c'
        self.reply = dict()


    def plot(self, search_query):
        r = requests.get(f"http://www.omdbapi.com/?apikey={self.key}&t={search_query}")
        data = json.loads(r.text)
        try:
            title = data['Title']
            plot = data['Plot']
            poster = data['Poster']
        except Exception:
            pass

        text = f"The plot of the movie {title} is, {plot}"
        self.reply = {'data': text, 'poster': poster}
        return self.reply

    def rating(self, search_query):
        r = requests.get(f"http://www.omdbapi.com/?apikey={self.key}&t={search_query}")
        data = json.loads(r.text)
        try:
            title = data['Title']
            imdbrating = data['imdbRating']
            poster = data['Poster']
            rating1_name = None
            rating1_value = None
        except Exception:
            pass
        try:
            rating1_name = data['Ratings'][1]['Source']
            rating1_value = data['Ratings'][1]['Value']
        except:
            pass

        if rating1_name and rating1_value is not None:
            text = f"{title} has a {rating1_name} score of {rating1_value}! and has an I.M.D.B rating of {imdbrating}!"
            self.reply = {'data': text, 'poster': poster}
            return self.reply
        else:
            text = f"{title} has an I.M.D.B rating of {imdbrating}!"
            self.reply = {'data': text, 'poster': poster}
            return self.reply


    def genre(self, search_query):
        r = requests.get(f"http://www.omdbapi.com/?apikey={self.key}&t={search_query}")
        data = json.loads(r.text)
        try:
            title = data['Title']
            genre = data['Genre']
            poster = data['Poster']
        except Exception:
            pass
        text = f"{title} consist of {genre}"
        self.reply = {'data': text, 'poster': poster}
        return self.reply


    def cast(self, search_query):
        r = requests.get(f"http://www.omdbapi.com/?apikey={self.key}&t={search_query}")
        data = json.loads(r.text)
        try:
            title = data['Title']
            director = data['Director']
            cast = data['Actors']
            poster = data['Poster']
        except Exception:
            pass
        text = f"The cast of {title} is {cast} and is directed by {director}"
        self.reply = {'data': text, 'poster': poster}
        return self.reply


    def movie(self, search_query):
        r = requests.get(f"http://www.omdbapi.com/?apikey={self.key}&t={search_query}")
        data = json.loads(r.text)
        try:
            title = data['Title']
            cast = data['Actors']
            poster = data['Poster']
            plot = data['Plot']
            released = data['Released']
            imdbrating = data['imdbRating']
            rating1_name = None
            rating1_value = None
        except Exception:
            pass
        try:
            rating1_name = data['Ratings'][1]['Source']
            rating1_value = data['Ratings'][1]['Value']
        except:
            pass

        if rating1_name is not None:
            text = f"{title} starring {cast} was Released on {released}. The plot of the movie is {plot}. It has a {rating1_name} score of {rating1_value}! and has an IMDB rating of {imdbrating}!"
            reply = {'data': text, 'poster': poster}
            return reply
        else:
            text = f"{title} starring {cast} was Released on {released}. The plot of the movie is {plot}. It has an IMDB rating of {imdbrating} "
            reply = {'data': text, 'poster': poster}
            return reply


if __name__ == "__main__":
    ob = Movie()
    speech = Speech('a40fb4ee-2f84-47ab-acce-c2828b277b08', '1jQFSMbVBjiX')
    data = ob.plot(input("movie name:"))
    info = data['data']
    print(info)
    poster = data['poster']
    body = {'url': poster}
    requests.post("http://localhost:8080/image", data=json.dumps(body))