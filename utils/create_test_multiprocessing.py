from pydub import AudioSegment
from pathlib import Path, PurePosixPath
from utils.conf.create_test_files import *
from shutil import copyfile
from multiprocessing import Pool


def place_dir_data():
    """ find directory data for placing files for text """
    p = Path('..')
    find_place_dir = list(p.glob('data'))[0].resolve()
    return find_place_dir


def mp3_to_wav(file):
    """ convert audio format from mp3 to wav and copy text file with correct answer """
    wav_file = new_dir.joinpath(PurePosixPath(file).name).with_suffix('.wav')
    copyfile(str(PurePosixPath(file).with_suffix('.txt')), str(wav_file.with_suffix('.txt')))
    sound = AudioSegment.from_mp3(file)
    sound.export(wav_file, format="wav")


def create_test_dataset_multiproc():
    """ create dir of wav files for test and demo """
    mp3_files = sorted(Path(source_directory).rglob('*.mp3'))[:number_test_files]
    pool = Pool()
    res = pool.map(mp3_to_wav, mp3_files)
    pool.close()
    pool.join()


if __name__ == '__main__':
    new_dir = Path(place_dir_data()).joinpath(PurePosixPath(target_directory).stem)
    new_dir.mkdir(parents=True, exist_ok=True)
    create_test_dataset_multiproc()
