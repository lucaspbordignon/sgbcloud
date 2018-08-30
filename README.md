# sgbcloud
Word cloud generator workflow, used on the 2018 edition of the
[Social Goods Brasil Festival](https://socialgoodbrasil.org.br/festival).

## Executing

The workflow to run the application is the following. Firt we need to install the
dependencies:

```
pip install -r requirements.txt
```

After that, we need to add the Google Cloud credentials to the given computer. To the usage of Google Cloud Speech API, instructions can be found [here](https://cloud.google.com/sdk/docs/quickstarts), following the right platform you are using.

After that, simply execute the recognition algorithm, from the root of the repository:

```
python run.py
```

## Resources
[SpeechRecognition](https://github.com/Uberi/speech_recognition)

[Snowboy](http://docs.kitt.ai/snowboy/#introduction) - It's not open source, but is an alternative

[Kaldi](https://github.com/pykaldi/pykaldi)

[NLTK](https://www.nltk.org/)

[PocketSphinx](https://github.com/bambocher/pocketsphinx-python)

[WaveNet](https://github.com/buriburisuri/speech-to-text-wavenet)
