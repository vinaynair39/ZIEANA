from os.path import join
import os
from watson_developer_cloud import TextToSpeechV1
from pydub import AudioSegment
from pydub.playback import play

user = 'c0acb244-5242-467c-b48f-2d8448b8fc9c'
password = 'Neru55aYWhz5'

text_to_speech = TextToSpeechV1(username=user, password=password)
path = join(os.getcwd(), 'output.mp3')

text = 'hello'
# text = '<speak><express-as type="Apology">I am so sorry. I\'m unable to find what you requested. what can i do to make it up to you?</express-as></speak>'
with open(path, 'wb') as audio_file:
    audio_file.write(
        text_to_speech.synthesize(text, accept='audio/mp3', voice="en-US_AllisonVoice"))

song = AudioSegment.from_mp3(path)
play(song)
os.remove(path)

