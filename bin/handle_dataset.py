import os
import io
from pathlib import Path
from multiprocessing import Pool
from utils.cloud.crt_api import CrtClient


def work_with_dataset(client, dir_dataset, suffix):
    """ working with files """
    assert os.path.exists(dir_dataset)
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
    file, suffix = args
    client = CrtClient(credentials='conf/crt_api_credentials.json')
    result = client.submit(file)
    record_result_recognize(result, Path(file).with_suffix(suffix))


def work_with_dataset_multi(dir_dataset, suffix):
    """ working with files """
    assert os.path.exists(dir_dataset)
    wav_files = sorted(Path(dir_dataset).rglob('*.wav'))
    pool = Pool()
    results = pool.map(work_for_each, [(file, suffix)
                                       for file in wav_files if is_need_again(Path(file).with_suffix(suffix))])
    pool.close()
    pool.join()
