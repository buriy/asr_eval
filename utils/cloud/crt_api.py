# cd /home/usr/stc-speechkit-python/    https://github.com/STC-VoiceKey/stc-speechkit-python
# cd asr
# python3 setup.py install

import io
import os
import logging
import base64
import json

from cloud_client.api import RecognizeApi
from cloud_client.models.audio_file_dto import AudioFileDto
from cloud_client.models.sessionless_recognition_request_dto import SessionlessRecognitionRequestDto
from cloud_client.models.start_session_request import StartSessionRequest
from cloud_client.models.recognition_request_dto import RecognitionRequestDto
from bin.handle_dataset import work_with_dataset

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(message)s')
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
speech_log = logging.FileHandler('crt_speech.log')
speech_log.setLevel(logging.INFO)
logger.addHandler(speech_log)


class CrtClient:

    def __init__(self, credentials='conf/crt_api_credentials.json'):
        self.credentials = json.load(open(credentials, 'rb'))
        self.recognize_api = RecognizeApi()
        self.credentials = StartSessionRequest(self.credentials['username'],
                                               self.credentials['password'],
                                               self.credentials['domain_id'])

    def submit(self, file_name):
        # Loads the audio into memory
        assert os.path.exists(file_name)
        with io.open(file_name, "rb") as in_file:
            data = in_file.read()
        encoded_string = base64.standard_b64encode(data)
        audio_file = AudioFileDto(encoded_string.decode('utf-8'), "audio/x-wav")
        try:
            # Detects speech in the audio file
            recognition_request = RecognitionRequestDto(audio_file, "CommonRus")
            self.sessionless_recognition_request = SessionlessRecognitionRequestDto(self.credentials, recognition_request)
            self.recognition_result = self.recognize_api.recognize_sessionless(self.sessionless_recognition_request)
            return ['OK', self.recognition_result.text]
        except Exception:
            print("Didn't work for:", file_name)
            import traceback;
            traceback.print_exc()
            return ['error', '']


if __name__ == '__main__':
    client = CrtClient(credentials='conf/crt_api_credentials.json')
    print(client.submit('data/examples/example_16000.wav')[1])           # it raw for test
    #work_with_dataset(client, 'data/test_wav_files', '.crt.txt')        # select this for working with dataset
