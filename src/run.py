import speech_recognition as sr


# Records the microphone audio
recognizer = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        print("Say something!")
        audio = recognizer.listen(source)

    # using Sphinx
    try:
        print("Sphinx thinks you said: " + r.recognize_sphinx(audio))
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
