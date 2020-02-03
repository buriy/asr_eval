# pip install --upgrade google-cloud-speech

import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import types


class GoogleClient:

    def __init__(self, sr=16000, premium=False, model='default', credentials='conf/google_api_credentials.json'):
        # Authorization json
        # Instantiates a client
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials
        self.client = speech.SpeechClient()
        self.config = speech.types.RecognitionConfig(encoding=speech.enums.RecognitionConfig.AudioEncoding.LINEAR16,
                                                     sample_rate_hertz=sr,
                                                     language_code='ru-RU',
                                                     # Enhanced models are only available to projects that
                                                     # opt in for audio data collection.
                                                     use_enhanced=premium,
                                                     # A model must be specified to use enhanced model.
                                                     model=model)

    def submit(self, file_name):
        # Loads the audio into memory
        assert os.path.exists(file_name)
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        try:
            # Detects speech in the audio file
            response = self.client.recognize(self.config, audio)
            # print(response)
            result = response.results
            if len(result) == 0:
                return '-'
            if len(result[0].alternatives) == 0:
                return '-'
            return result[0].alternatives[0].transcript
        except Exception:
            print("Didn't work for:", file_name)
            import traceback;
            traceback.print_exc()
            return ''


if __name__ == '__main__':
    client = GoogleClient(credentials='conf/google_api_credentials.json')
    print(client.submit('data/examples/example_16000.wav'))
