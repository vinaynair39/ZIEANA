from pydub import AudioSegment
from pydub.playback import play
from os.path import join
import os
import urllib
import urllib.request
import urllib.parse
import re
import webbrowser
import threading
import requests
import json


class Performers:

    def play(self, file_name):

        path = join(os.getcwd(), 'music', file_name + '.mp3')
        print(path)
        song = AudioSegment.from_mp3(path)
        t = threading.Thread(target=play(song))
        t.start()



    def youtube_player(self, search_query):
        query_string = urllib.parse.urlencode({"search_query":search_query})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"/watch\?v=(.{11})', html_content.read().decode())
        resonse = "http://www.youtube.com/watch?v=" + search_results[0]
        print(resonse)
        webbrowser.open(resonse)

    def playlist(self, name):
        music_list = [
            "so far away"

        ]
        for i in music_list:
            if i.lower() == name.lower():
                print("okay")
                self.play(name)

    def find_images(self, search_word):
        headers = {'Api-Key': '8z76ceavpadeka7hrkze6kff'}
        r = requests.get(
            f'https://api.gettyimages.com/v3/search/images?file_types=jpg&minimum_size=xx_large&phrase={search_word}&sort_order=best_match',
            headers=headers
        )
        data = json.loads(r.text)
        image1 = data['images'][0]['display_sizes'][0]['uri']
        image2 = data['images'][1]['display_sizes'][0]['uri']
        return image1, image2



if __name__ == '__main__':
    test = Performers()
    image1 = test.find_images(input())
    print(image1)