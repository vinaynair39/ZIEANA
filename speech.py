import os
import pyaudio
import requests
import speech_recognition as sr
from os.path import join
from watson_developer_cloud import TextToSpeechV1
from pydub import AudioSegment
from pydub.playback import play




class Speech(object):

    def __init__(self, user, password,launch_phrase="mirror mirror", debugger_enabled=False):

        self.user = user
        self.password = password
        self.launch_phrase = launch_phrase
        self.debugger_enabled = debugger_enabled
        self.__debugger_microphone(enable=False)

    def listen_to_voice(self):  # obtain audio from the microphone

        # Creates a new Recognizer instance, which represents a collection of speech recognition functionality.
        r = sr.Recognizer()
        # Creates a new Microphone instance, which represents a physical microphone on the computer.
        m = sr.Microphone()

        with m as source:   # open the microphone and start recording, source is the microphone(m's) instance
            r.adjust_for_ambient_noise(source)
            r.dynamic_energy_threshold = True
            r.pause_threshold = 1.4    # minimum length of silence (in sec) that will be considered as the end of phrase
            self.__debugger_microphone(enable=True)
            print("I'm listening")
            audio = r.listen(source)

        self.__debugger_microphone(enable=True)
        print("Found audio")
        return r, audio

    def google_speech_recognition(self, recognizer, audio):
        speech = None
        try:
            speech = recognizer.recognize_google(audio)
            print("Zieana thinks you said " + speech)
        except sr.UnknownValueError:
            print("Zieana could not understand what you said")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))
        if speech is None:
            no_text = "Couldn't receive any vocals. Please try again!"
            print(no_text)
            self.text_to_speech(no_text)
        else:
            return speech

    def is_call_to_action(self, recognizer, audio):
        speech = self.google_speech_recognition(recognizer, audio)

        if speech is not None and self.launch_phrase in speech.lower():
            return True

        return False

    def __debugger_microphone(self, enable=True):
        if self.debugger_enabled:
            try:
                r = requests.get("http://localhost:8080/microphone?enabled=%s" % str(enable))
                if r.status_code != 200:
                    print("Used wrong endpoint for microphone debugging")
            except Exception as e:
                print(e)

    def text_to_speech(self, text):  # converts the given text to vocals using IBM watson

        text = text
        text_to_speech = TextToSpeechV1(username=self.user, password=self.password)
        path = join(os.getcwd(), 'output.mp3')

        # synthesize method returns bytes of audio so we have to write it inside a file
        with open(path, 'wb') as audio_file:
            audio_file.write(
                text_to_speech.synthesize(text, accept='audio/mp3', voice="en-US_AllisonVoice"))

        # playing the created vocals
        voice = AudioSegment.from_mp3(path)
        play(voice)
        os.remove(path)


if __name__ == '__main__':
    test = Speech('c0acb244-5242-467c-b48f-2d8448b8fc9c', 'Neru55aYWhz5')
    recognizer, audio = test.listen_to_voice()
    speech = test.google_speech_recognition(recognizer, audio)
    text = speech + ' was said by ziana. period!'

    test.text_to_speech(text)






