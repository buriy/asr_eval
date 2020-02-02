import os
import traceback
import json
from pathlib import Path
from wit import Wit


class WitClient:
    def __init__(self, credentials='conf/wit_api_credentials.json'):
        ind = 0 if Path('.').resolve().stem == 'bin' else 1
        credentials = sorted(Path('.').resolve().parents[ind].rglob(credentials))[0]
        self.credentials = json.load(open(credentials, 'r'))
        self.client = Wit(self.credentials['secret'])

    def submit(self, file_name):
        assert os.path.exists(file_name)
        with open(file_name, 'rb') as f:
            try:
                resp = self.client.speech(f, None, {'Content-Type': 'audio/wav'})
                return str(resp['_text']) or '-'
            except Exception:
                traceback.print_exc()
                return ''


if __name__ == '__main__':
    client = WitClient()
    print(client.submit('data/examples/example_16000.wav'))
