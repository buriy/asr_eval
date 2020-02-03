import sys
import os
from pydub import AudioSegment
from pathlib import Path
from shutil import copyfile

args = sys.argv
TARGET_DIR = '../data/files/'
MAX_FILES = 100


def mp3_to_wav(file, new_dir):
    """ convert audio format from mp3 to wav and copy text file with correct answer """
    wav_file = (new_dir/Path(file).name).with_suffix('.wav')
    copyfile(str(Path(file).with_suffix('.txt')), str(wav_file.with_suffix('.txt')))
    sound = AudioSegment.from_mp3(file)
    sound.export(wav_file, format="wav")


def create_test_dataset(new_dir):
    """ create dir of wav files for test and demo """
    mp3_files = sorted(Path(SOURCE_DIR).rglob('*.mp3'))[:MAX_FILES]
    for file in mp3_files:
        mp3_to_wav(file, new_dir)


if __name__ == '__main__':
    if len(args) == 2:
        SOURCE_DIR = sys.argv[1]
        assert os.path.exists(SOURCE_DIR)
        new_dir = Path(TARGET_DIR).parent.resolve() / Path(TARGET_DIR).parts[-1]
        new_dir.mkdir(parents=True, exist_ok=True)
        create_test_dataset(new_dir)
    else:
        print('Please run program with one argument - directory name (place for dataset locate)!')
