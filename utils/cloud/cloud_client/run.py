import base64
from cloud_client.models.auth_request_dto import AuthRequestDto
from cloud_client.api.session_api import SessionApi
from cloud_client.api import PackagesApi
from cloud_client.api import RecognizeApi
from cloud_client.models.audio_file_dto import AudioFileDto
from cloud_client.models.recognition_request_dto import RecognitionRequestDto

session_api = SessionApi()
credentials = AuthRequestDto("username", 261, "password")
session_id = session_api.login(credentials).session_id
packages_api = PackagesApi()
packages_api.load(session_id, "CommonRus").status
in_file = open("F:\\Art\\0068_20170407_own_6944_181007-1496930080.wav", "rb")
data = in_file.read()
in_file.close()
encoded_string = base64.standard_b64encode(data)
string = str(encoded_string, 'ascii', 'ignore')
recognize_api = RecognizeApi()
audio_file = AudioFileDto(string, "audio/x-wav")
recognition_request = RecognitionRequestDto(audio_file, "CommonRus")
recognition_result = recognize_api.recognize(session_id, recognition_request)
print(recognition_result)
