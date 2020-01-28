#! /usr/bin/env python3
from utils.cloud.tinkoff.audio import audio_open_read
from utils.cloud.tinkoff.auth import authorization_metadata
from utils.cloud.tinkoff.cloud.stt.v1 import stt_pb2
from utils.cloud.tinkoff.cloud.stt.v1 import stt_pb2_grpc
from utils.cloud.tinkoff.common import build_recognition_request, make_channel, print_recognition_response, \
    BaseRecognitionParser


def main():
    args = BaseRecognitionParser().parse_args()
    if args.encoding == stt_pb2.RAW_OPUS:
        raise ValueError("RAW_OPUS encoding is not supported by this script")
    with audio_open_read(args.audio_file, args.encoding, args.rate, args.num_channels, args.chunk_size,
                         args.pyaudio_max_seconds) as reader:
        stub = stt_pb2_grpc.SpeechToTextStub(make_channel(args))
        metadata = authorization_metadata(args.api_key, args.secret_key, "tinkoff.cloud.stt")
        response = stub.Recognize(build_recognition_request(args, reader), metadata=metadata)
        print_recognition_response(response)


if __name__ == "__main__":
    main()

