#pip install --upgrade google-cloud-speech

import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

class GoogleClient:
    def __init__(self, sr=16000,premium=False,model='default'):
        #Authorization json
        os.environ['GOOGLE_APPLICATION_CREDENTIALS']='conf/google_api_credentials.json'
        # Instantiates a client
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
            #print(response)
            result = response.results[0].alternatives[0].transcript
            
            return result
        
        except Exception:
            import traceback; traceback.print_exc()
            print("Didn't work for:", file_name)
            return ''
        
        
if __name__ == '__main__':
    client = GoogleClient()
    print(client.submit('data/examples/example_16000.wav'))
                         
    
