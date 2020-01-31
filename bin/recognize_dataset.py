import os
import io
from pathlib import Path
from multiprocessing import Pool


def create_client(name_api):
    name_api = name_api.lower()
    if name_api == 'crt':
        from utils.cloud.crt_api import CrtClient
        client = CrtClient(credentials='conf/crt_api_credentials.json')
    elif name_api == 'google':
        from utils.cloud.google_api import GoogleClient
        client = GoogleClient(credentials='conf/google_api_credentials.json')
    elif name_api == 'wit':
        from utils.cloud.wit_ai import WitClient
        client = WitClient(WIT_SECRET='HOUUWVT2MFFIF5NRN5V2XP7UL4EKIXCU')
    elif name_api == 'tinkoff':
        from utils.cloud.tinkoff.tinkoff_api import TinkoffClient
        client = TinkoffClient()
    elif name_api == 'yandex':
        from utils.cloud.yandex_short import YandexClient
        client = YandexClient()
    else:
        client = False
    return client


def get_suffix(name_api):
    name_api = name_api.lower()
    if name_api == 'crt':
        suffix = '.crt.txt'
    elif name_api == 'google':
        suffix = '.google.txt'
    elif name_api == 'wit':
        suffix = '.wit.txt'
    elif name_api == 'tinkoff':
        suffix = '.tinkoff.txt'
    elif name_api == 'yandex':
        suffix = '.yandex.txt'
    else:
        suffix = False
    return suffix


def work_with_dataset(name_api, dir_dataset):
    """ working with files in mode one process """
    assert os.path.exists(dir_dataset)
    client = create_client(name_api)
    if not client:
        print("Error name api")
        return
    suffix = get_suffix(name_api)
    wav_files = sorted(Path(dir_dataset).rglob('*.wav'))
    for file in wav_files:
        if not is_need_again(Path(file).with_suffix(suffix)):
            continue
        result = client.submit(file)
        record_result_recognize(result, Path(file).with_suffix(suffix))


def record_result_recognize(result, res_name):
    """ save results  """
    with io.open(res_name, 'w') as f:
        if not len(result):
            f.close()
        else:
            f.write(result)


def is_need_again(file_name):
    """" check file for need recognition """
    if file_name.is_file() and file_name.stat().st_size > 0:
        return False
    else:
        return True


def work_for_each(args):
    """ work in each process """
    name_api, file, suffix = args
    client = create_client(name_api)
    result = client.submit(file)
    record_result_recognize(result, Path(file).with_suffix(suffix))


def work_with_dataset_multi(name_api, dir_dataset):
    """ working with files in mode multiprocessing"""
    assert os.path.exists(dir_dataset)
    client = create_client(name_api)                 # check is exists client for  name_api
    if not client:
        print("Error name api")
        return
    suffix = get_suffix(name_api)
    wav_files = sorted(Path(dir_dataset).rglob('*.wav'))
    pool = Pool()
    results = pool.map(work_for_each, [(name_api, file, suffix)
                                       for file in wav_files if is_need_again(Path(file).with_suffix(suffix))])
    pool.close()
    pool.join()


if __name__ == '__main__':
    work_with_dataset_multi('CRT', 'data/test_wav_files')
