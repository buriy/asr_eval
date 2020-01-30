import os
import io
from pathlib import Path


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
        if result[0] == 'error':
            f.close()
        elif result[0] == 'OK' and not len(result[1]):
            f.write('-')
        else:
            f.write(result[1])


def is_need_again(file_name):
    """" check file for need recognition """
    if file_name.is_file() and file_name.stat().st_size > 0:
        return False
    else:
        return True


