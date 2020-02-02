import json
import traceback
import urllib


class YandexClient:
    def __init__(self, auth_key=None, token=None):
        self.auth_key = auth_key
        self.auth_token = token

    def submit(self, f_wav, sr):
        with open(f_wav, "rb") as f:
            # skip wav header
            data = f.read()[44:]

        assert sr in [8000, 16000]
        params = "&".join([
            "topic=general",
            # "folderId=%s" % FOLDER_ID,
            "lang=ru-RU",
            "sampleRateHertz={}".format(sr),
            "format=lpcm"
        ])
        url = urllib.request.Request("https://stt.api.cloud.yandex.net/speech/v1/stt:recognize/?%s" % params, data=data)
        if self.auth_token:
            url.add_header("Authorization", "Bearer %s" % self.auth_token)
        if self.auth_key:
            url.add_header("Authorization", "Api-Key %s" % self.auth_key)

        try:
            responseData = urllib.request.urlopen(url).read().decode('UTF-8')
            decodedData = json.loads(responseData)

            if decodedData.get("error_code") is None:
                result = decodedData.get("result")
                return result or '-'
        except urllib.error.HTTPError:
            print("Didn't work for:", f_wav)
            import traceback; traceback.print_exc()
            return ''


if __name__ == '__main__':
    FOLDER_ID = "b1gfo8mbllav4m5tdqpn"  # Идентификатор каталога
    # IAM_TOKEN = "CggaATEVAgAAABKABE12Q9vqmctOwZL6IZz0AoFWDh3scKJKAGRuSLIWEcTiSQoN3V5kMuzEGlSzY7TEvb5_Bw3GLWdwWyfPC3uM3Brp5CRT6CjgY6ymCeB6JuI-R1WrOHQ854Lq5pzKyMMZj0dBi26v-NeZfAqN1UU3YPXXIg95780RtLTYYGJLw-R9T7GJKKM5JBDY5lH3xnrd_NVJQ69DoEtCRxv9hwEGAS5GM1Pg2xPBpPE_Mr8mtLrEwYooEUceh6rPNL9g_3BWkGks2tUwN02oAP1TpArKM2rpIxkfyxaqKAOgzn-Ws-HEfMV8moiLTfP8vppS8wXDBX_kpJAvC4j3-Yeo4qYXgh3AtlLccX992qB_zdPr9RM_M6uCS8xufzJd5rBOnx8Yfz5HhjOSaDx45O8vZNLvWbQy4VoonU5gLPcjl3xmgZxr7o24d9sHwfMO5lcqh5oATtp1MGoWWMmgdob80N7kGndabv1_Tz0oR18VoVUEuCC-JlZZnFkJ2UPuCCHDP4QJ2pGl-sNrEmcq_yQx7u35hCKXtC0ZptOTYVv4gmhls9c7QDCrKxfCiSOyLFFPSgG5vA4QaWWwgEJ7HQtSJpioFVoeOp6fzNSrYQMqM_94ucvEa1s4zgzUkZHFD856FcG0raexvBSg2tYCDJ74HVB4KAJ6KgpRy3kQlcg5t_Y6SxX_GmsKIDg4ZGI2MWE5YWU1ZDRkZDg5ODI2ZDEwYzljMTdiMTFhEJDIhOQFGNCZh-QFIikKFGFqZXRpN2pnMzhkZWgwbGkyanBlEhFtYWtzaW1vdi5iZWxnb3JvZFoAMAI4AUoIGgExFQIAAABQASD6BA" # IAM-токен
    # AUTH_ID = 'ajenfj2500ep5ta6d94o'
    AUTH_KEY = 'AQVN13zEUAHZL1RmpJjRHcj6QhZKuFgiHqEcdoQH'
    YandexClient(AUTH_KEY)