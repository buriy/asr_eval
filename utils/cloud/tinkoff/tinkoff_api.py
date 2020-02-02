#! /usr/bin/env python3
import os
import json
from pathlib import Path

from utils.cloud.tinkoff.audio import audio_open_read
from utils.cloud.tinkoff.auth import authorization_metadata
from utils.cloud.tinkoff.cloud.stt.v1 import stt_pb2
from utils.cloud.tinkoff.cloud.stt.v1 import stt_pb2_grpc
from utils.cloud.tinkoff.common import build_recognition_request, make_channel, print_recognition_response, \
    BaseRecognitionParser


class TinkoffClient:

    def __init__(self, credentials='conf/tinkoff_api_credentials.json'):
        ind = 0 if Path('.').resolve().stem == 'bin' else 2
        credentials = sorted(Path('.').resolve().parents[ind].rglob(credentials))[0]
        self.credentials = json.load(open(credentials, 'rb'))
        os.environ['VOICEKIT_SECRET_KEY'] = self.credentials['secret_key']
        os.environ['VOICEKIT_API_KEY'] = self.credentials['api_key']
        self.args_input = ['-r', '16000', '-c', '1', '-e', 'LINEAR16']
        # FIXME: set other attributes needed at submit()
        # FIXME: they are set up at BaseRecognitionParser
        # self.encoding = stt_pb2.LINEAR16
        # encoding = ProtobufEnumChoices(stt_pb2.AudioEncoding,
        #                                ["MPEG_AUDIO", "LINEAR16", "ALAW", "MULAW", "RAW_OPUS"])
        # self.add_argument("-r", "--rate", type=int, required=True, help="Audio sampling rate.")
        # self.add_argument("-c", "--num_channels", type=int, required=True, help="Number of audio channels.")
        # self.add_argument("-e", "--encoding", type=encoding, required=True, help="Audio encoding.", choices=encoding)
        # self.add_argument("--max_alternatives", type=int, default=1, help="Number of speech recognition alternatives "
        #                   "to return.")
        # self.add_argument("--do_not_perform_vad", action='store_true',
        #                   help="Specify this to disable voice activity detection. All audio is processed "
        #                   "as though it were a single utterance.")
        # self.add_argument("--silence_duration_threshold", type=float, default=0.6,
        #                   help="Silence threshold in seconds for VAD to assume the current utterance is ended and "
        #                   "the next utterance shall begin.")
        # self.add_argument("--language_code", type=str, choices=["ru-RU"], default="ru-RU",
        #                   help="Language for speech recognition.")
        # self.add_argument("--disable_automatic_punctuation", action="store_true",
        #                   help="Specify this to disable automatic punctuation in recognition results.")
        # self.add_argument("--chunk_size", type=int, default=1024, help="Chunk size for streaming")
        # self.add_argument("--pyaudio_max_seconds", type=float, default=None, help="Maximum length of pyaudio "
        #                   "recording in seconds.")
        # self.add_argument("audio_file", type=str, help="Audio file to recognize or 'pyaudio:' to use stream from mic.")
        # config.encoding = args.encoding
        # config.sample_rate_hertz = args.rate
        # config.num_channels = args.num_channels
        # config.max_alternatives = args.max_alternatives
        # if args.do_not_perform_vad:
        #     config.do_not_perform_vad = args.do_not_perform_vad
        # else:
        #     config.vad_config.silence_duration_threshold = args.silence_duration_threshold
        # config.language_code = args.language_code
        # config.enable_automatic_punctuation = not args.disable_automatic_punctuation

    def submit(self, file_name):
        args = BaseRecognitionParser().parse_args([*self.args_input, file_name])
        if args.encoding == stt_pb2.RAW_OPUS:
            raise ValueError("RAW_OPUS encoding is not supported by this script")
        with audio_open_read(file_name, args.encoding, args.rate, args.num_channels, args.chunk_size,
                             args.pyaudio_max_seconds) as reader:
            try:
                stub = stt_pb2_grpc.SpeechToTextStub(make_channel(args))
                metadata = authorization_metadata(args.api_key, args.secret_key, "tinkoff.cloud.stt")
                response = stub.Recognize(build_recognition_request(args, reader), metadata=metadata)
                return print_recognition_response(response) or '-'
            except Exception:
                print("Didn't work for:", file_name)
                import traceback;
                traceback.print_exc()
                return ''


if __name__ == "__main__":
    client = TinkoffClient()
    print(client.submit('data/examples/example_16000.wav'))

