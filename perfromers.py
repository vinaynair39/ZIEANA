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







if __name__ == '__main__':
    test = Performers()
    test.playlist(input())