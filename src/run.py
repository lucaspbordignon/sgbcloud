import speech_recognition as sr


# Records the microphone audio
recognizer = sr.Recognizer()

API_KEY = r""""MY_KEY"""

while True:
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)

    # using Sphinx
    try:
        print("Google thinks you said: " + recognizer.recognize_google_cloud(audio,
                                                                       language='pt-BR',
                                                                       credentials_json=API_KEY))
    except sr.UnknownValueError:
        print("Google could not understand audio")
    except sr.RequestError as e:
        print("Google error; {0}".format(e))
