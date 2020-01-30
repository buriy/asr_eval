# cd /home/usr/stc-speechkit-python/    https://github.com/STC-VoiceKey/stc-speechkit-python
# cd asr
# python3 setup.py install

import io
import os
from pathlib import Path
import logging
import base64
import json

from cloud_client.api import RecognizeApi
from cloud_client.models.audio_file_dto import AudioFileDto
from cloud_client.models.sessionless_recognition_request_dto import SessionlessRecognitionRequestDto
from cloud_client.models.start_session_request import StartSessionRequest
from cloud_client.models.recognition_request_dto import RecognitionRequestDto

logging.basicConfig(level=logging.INFO, format='%(asctime)s-%(message)s')
logger = logging.getLogger(__file__)
logger.setLevel(logging.INFO)
speech_log = logging.FileHandler('crt_speech.log')
speech_log.setLevel(logging.INFO)
logger.addHandler(speech_log)


class CrtClient:

    def __init__(self,
                 credentials='conf/crt_api_credentials.json',
                 suffix_service=".crt.txt",
                 dir_dataset='../data/files'):
        self.credentials = json.load(open(credentials, 'rb'))
        self.recognize_api = RecognizeApi()
        self.credentials = StartSessionRequest(self.credentials['username'],
                                               self.credentials['password'],
                                               self.credentials['domain_id'])
        self.suffix = suffix_service
        self.dir_dataset = dir_dataset

    def submit(self, file_name):
        # Loads the audio into memory
        assert os.path.exists(file_name)
        if not self.is_need_again(file_name):    # this file was recognized early and saved result
            return
        with open(file_name, "rb") as in_file:
            data = in_file.read()
        encoded_string = base64.standard_b64encode(data)
        audio_file = AudioFileDto(encoded_string.decode('utf-8'), "audio/x-wav")
        try:
            # Detects speech in the audio file
            recognition_request = RecognitionRequestDto(audio_file, "CommonRus")
            self.sessionless_recognition_request = SessionlessRecognitionRequestDto(self.credentials, recognition_request)
            self.recognition_result = self.recognize_api.recognize_sessionless(self.sessionless_recognition_request)
            self.record_result_recognize(file_name, ['OK', self.recognition_result.text])
        except Exception:
            self.record_result_recognize(file_name, ['error', ''])
            print("Didn't work for:", file_name)
            import traceback;
            traceback.print_exc()
            return ''

    def record_result_recognize(self, name_file, result):
        """ save results  """
        res_name = Path(name_file).with_suffix(self.suffix)
        with io.open(res_name, 'w') as f:
            if result[0] == 'error':
                f.close()
            elif result[0] == 'OK' and not len(result[1]):
                f.write('-')
            else:
                f.write(result[1])

    def is_need_again(self, file_name):
        """" check file for need recognition """
        nf = Path(file_name).with_suffix(self.suffix)
        if nf.is_file() and nf.stat().st_size > 0:
            return False
        else:
            return True

    def work_with_dataset(self):
        """ working with files """
        wav_files = sorted(Path(self.dir_dataset).rglob('*.wav'))
        for file in wav_files:
            if not self.is_need_again(file):
                continue
            self.submit(file)


if __name__ == '__main__':
    client = CrtClient(suffix_service=".crt.txt", dir_dataset='/data/files')
    print(client.submit('data/examples/example_16000.wav'))      # it raw for test
    #work_with_dataset()                                                      # select this for working with dataset
