import pyaudio
import re
import sys

try:
    import google.cloud.speech as speech
except:
    import google.cloud.speech as speech

from google.cloud.speech import enums
from google.cloud.speech import types
from six.moves import queue


# Audio recording parameters
RATE = 16000
CHUNK = int(RATE / 10)  # 100ms


class MicrophoneStream(object):
    '''
        Opens a recording stream as a generator yielding the audio recorded
    (in chunks).
    '''
    def __init__(self, rate, chunk):
        self._rate = rate
        self._chunk = chunk

        self._buff = queue.Queue() # Audio data buffer
        self._closed = True

    def __enter__(self):
        '''
            Run the audio stream asynchronously to fill the buffer object.
        Called when using inside a "with" scope.
        '''
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1, rate=self._rate,
            input=True, frames_per_buffer=self._chunk,
            stream_callback=self._fill_audio_buffer,
        )

        self._closed = False

        return self

    def __exit__(self, type, value, traceback):
        self._audio_stream.stop_stream()
        self._audio_stream.close()
        self._closed = True
        self._buff.put(None)
        self._audio_interface.terminate()

    def _fill_audio_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)

        return None, pyaudio.paContinue

    def generator(self):
        '''
            Generator used to iterate over the audio input. Yields chunks of
        data read from the microphone.
        '''
        while not self._closed:
            chunk = self._buff.get() # get() is a blocking call to the queue

            if chunk is None:
                return

            data = [chunk]

            # Consumes already buffered data
            while True:
                try:
                    chunk = self._buff.get(block=False)
                    if chunk is None:
                        return
                    data.append(chunk)
                except queue.Empty:
                    break

            yield b''.join(data)



class Recognizer(object):
    def __init__(self, language_code='pt-BR',filename='speech.txt'):
        self._language_code = language_code
        self._client = speech.SpeechClient()
        self._filename = filename
        self._config = types.RecognitionConfig(
                        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
                        sample_rate_hertz=RATE,
                        language_code=language_code)
        self._streaming_config = types.StreamingRecognitionConfig(
                                    config=self._config,
                                    interim_results=True)


    def recognize(self):
        try:
            self._make_requests(self._client,
                                self._config,
                                self._streaming_config)
        except:
            print('############')
            print('Time exceeded from request! Making another one!')
            self.recognize()

    def _fetch_data_from_requests(self, responses):
        '''
            Given a list of requests to the GCS API, fetch and clean the
        data coming from it.
        '''
        chars_printed_count = 0
        backup = ['']

        for response in responses:
            try:
                if not response.results:
                    continue

                result = response.results[0]

                if not result.alternatives:
                    continue

                # Display the transcription of the most likely alternative
                transcript = result.alternatives[0].transcript

                overwrite_chars = ' ' * (chars_printed_count - len(transcript))

                # is_final results are "complete" phrases, detected by the API
                if not result.is_final:
                    sys.stdout.write(transcript + overwrite_chars + '\r')
                    sys.stdout.flush()

                    chars_printed_count = len(transcript)
                else:
                    # Backup the file on a simple .txt file after finished
                    # phrases
                    backup = [transcript + overwrite_chars]

                    with open(self._filename, 'a') as file:
                        file.writelines([transcript + overwrite_chars])

                    # Exit recognition if we say batman
                    if re.search(r'\b(batman)\b', transcript, re.I):
                        print('Batman has been called. Exiting...')
                        break

                    chars_printed_count = 0
            except:
                # If we exceed the time limit for the API request, save the
                # context and raise the error
                with open(self._filename, 'a') as file:
                    file.writelines(backup)

                raise

    def _make_requests(self, client, config, streaming_config):
        '''
            Execute the requests to the Google Cloud Speech API, given
        the audio input from the microphone.
        '''
        with MicrophoneStream(RATE, CHUNK) as stream:
            audio_generator = stream.generator()
            requests = (types.StreamingRecognizeRequest(audio_content=content)
                        for content in audio_generator)

            responses = client.streaming_recognize(streaming_config, requests)

            self._fetch_data_from_requests(responses)


if __name__ == '__main__':
    recognizer = Recognizer()
    recognizer.recognize()
