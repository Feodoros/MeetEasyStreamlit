import json
import os
import assembly_recognition

DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(DIR, 'data')


input_path = os.path.join(
    DATA_DIR, 'gentle learning w_ Dima.mp3')
output_path = os.path.join(DATA_DIR, f'{os.path.basename(input_path)}.json')


if __name__ == '__main__':
    assembly = True
    transcript_json = {}

    if assembly:
        # AssemblyAI
        transcript_json = assembly_recognition.transcribe_meeting(input_path)
    else:
        # Yandex Speech-kit
        #transcript_json = transcriber.transcribe_meeting(input_path)
        pass

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(transcript_json, f, ensure_ascii=False)
