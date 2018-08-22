import speech_recognition as sr


class AudioRecognizer():
    API_KEY = r""""MY_KEY"""

    def __init__(self):
        self.recognizer = sr.Recognizer()

    def recognize(source='microphone'):
        sourceFunction = sr.Microphone if source == 'microphone' else sr.AudioFile

        while True:
            with sourceFunction() as source:
                print("Say something!")
                audio = self.recognizer.listen(source)

            # Using Google Cloud Speech API
            try:
                print("Google thinks you said: " + \
                        self.recognizer.recognize_google_cloud(audio,
                                                               language='pt-BR',
                                                               credentials_json=self.API_KEY))
            except sr.UnknownValueError:
                print("Google could not understand audio")
            except sr.RequestError as e:
                print("Google error; {0}".format(e))
