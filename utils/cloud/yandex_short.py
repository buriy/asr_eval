import os
import json
import requests
import sox


class YandexClient:

    def __init__(self, credentials='conf/yandex_api_credentials.json'):
        self.credentials = json.load(open(credentials, 'rb'))
        self.auth_key = self.credentials["AUTH_KEY"]
        self.folder_id = self.credentials["FOLDER_ID"]

    def get_token(self):
        params = {'yandexPassportOauthToken': self.auth_key}
        response = requests.post('https://iam.api.cloud.yandex.net/iam/v1/tokens', params=params)
        decode_response = response.content.decode('UTF-8')
        text = json.loads(decode_response)
        iam_token = text.get('iamToken')
        return iam_token

    def submit(self, file_name):
        sample_rate = int(sox.file_info.sample_rate(file_name))
        with open(file_name, "rb") as f:
            # skip wav header
            data_sound = f.read()[44:]

        assert sample_rate in [8000, 16000]
        iam_token = self.get_token()
        headers = {'Authorization': f'Bearer {iam_token}'}
        params = {
            'lang': 'ru-RU',
            'folderId': self.folder_id,
            'format': 'lpcm',
            'sampleRateHertz': sample_rate,
        }
        URL_REC = 'https://stt.api.cloud.yandex.net/speech/v1/stt:recognize'

        try:
            response = requests.post(URL_REC, params=params, headers=headers, data=data_sound)
            decode_resp = response.content.decode('UTF-8')
            text = json.loads(decode_resp)
            return text['result'] or '-'
        except Exception:
            print("Didn't work for:", file_name)
            import traceback;
            traceback.print_exc()
            return ''


if __name__ == '__main__':
    client = YandexClient()
    print(client.submit('data/examples/example_16000.wav'))
