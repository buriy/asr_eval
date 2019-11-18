import traceback

from wit import Wit


class WitClient:
    def __init__(self, WIT_SECRET):
        self.client = Wit(WIT_SECRET)

    def submit(self, wav_fn):
        with open(wav_fn, 'rb') as f:
            try:
                resp = self.client.speech(f, None, {'Content-Type': 'audio/wav'})
                #print(repr(resp))
                return str(resp['_text'])
            except Exception:
                traceback.print_exc()
                return ''

if __name__ == '__main__':
    example = '../../dsdata/real/iqspeech-1/sample-1/0000.wav'
    WIT_SECRET = 'HOUUWVT2MFFIF5NRN5V2XP7UL4EKIXCU'
    wit = WitClient(WIT_SECRET)
    print(example, repr(wit.submit(example)))
