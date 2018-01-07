from pydub import AudioSegment
from pydub.playback import play
from os.path import join
import os
import urllib
import urllib.request
import urllib.parse
import re
import webbrowser


class Performers:

    def play(self, file_name):
        path = join(os.getcwd(), file_name)
        song = AudioSegment.from_mp3(path)
        play(song)

    def youtube_player(self, search_query):
        query_string = urllib.parse.urlencode({"search_query":search_query})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"/watch\?v=(.{11})', html_content.read().decode())
        resonse = "http://www.youtube.com/watch?v=" + search_results[0]
        print(resonse)
        webbrowser.open(resonse)


if __name__ == '__main__':
    test = Performers()
    test.youtube_player()