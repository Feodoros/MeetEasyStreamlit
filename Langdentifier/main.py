import os
from lang_identification import *
import subprocess

DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(DIR, '../../Transcriber')


input_path = os.path.join(
    DATA_DIR, 'call7.webm')

dotsplit = input_path.split('.')

shortened_path = ".".join(dotsplit[:-1])+'_shortened.'+dotsplit[-1]


if __name__ == '__main__':

    subprocess.call(['ffmpeg', '-i', input_path,'-to','20','-c', 'copy', shortened_path])
    if dotsplit[-1]!='wav':
        wav_path = ".".join(shortened_path.split('.')[:-1]+['wav'])
        subprocess.call(['ffmpeg', '-i', shortened_path,'-acodec','pcm_u8','-ar', '16000', wav_path])

        wav = read_audio(wav_path, sampling_rate=SAMPLING_RATE)
        os.remove(wav_path)
    else:
        wav = read_audio(shortened_path, sampling_rate=SAMPLING_RATE)
    lang = get_language(wav, model)
    print(lang)
    os.remove(shortened_path)
