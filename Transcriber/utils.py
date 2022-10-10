import time
import requests
from datetime import timedelta
from pydub import AudioSegment
# from pyannote.audio import Pipeline

# = Pipeline.from_pretrained("pyannote/speaker-diarization")


def load_mp3_to_bucket(mp3_path, new_name, client, bucket_name):
    try:
        audio_in = AudioSegment.from_file(mp3_path)
        audio_out = audio_in.export(new_name, format='ogg', codec='libopus')
        put_object_output = client.put_object(
            Bucket=bucket_name, Key=new_name, Body=audio_out)
        return put_object_output['ResponseMetadata']
    except Exception as e:
        return {'HTTPStatusCode': 404, 'Error': str(e)}


def get_audio_recognition(name, api_key, post, bucket_name):
    filelink = 'https://storage.yandexcloud.net/%s/%s' % (bucket_name, name)

    body = {
        "config": {
            "specification": {
                "languageCode": "ru-RUS",
            }
        },
        "audio": {
            "uri": filelink
        }
    }
    header = {'Authorization': 'Api-Key {}'.format(api_key)}

    req = requests.post(post, headers=header, json=body)
    data = req.json()

    if 'id' in data.keys():
        data_id = data['id']
        print('Transcription request %s in progress' % data_id)

        while True:
            time.sleep(3)

            GET = "https://operation.api.cloud.yandex.net/operations/{id}"
            req = requests.get(GET.format(id=data_id), headers=header)
            req = req.json()

            if req['done']:
                break
            print('...')

        print('Done')
        return req

    return {'error': data}


def transcript_to_json(transcript, voice_time_json):
    def getOverlap(a, b):
        return max(0, min(a[1], b[1]) - max(a[0], b[0]))
    
    default_speaker = "A"

    voices = bool(voice_time_json)
    transcript_json = {'recording_id': transcript['id']}
    if voices:
        voice_chunks = voice_time_json['chunks']
    messages = []
    k = 0
    #prev_speaker = ''
    for i in range(0, len(transcript['response']['chunks']), 2):
        chunk = transcript['response']['chunks'][i]

        start_time = float(chunk['alternatives'][0]
                           ['words'][0]['startTime'][:-1])
        end_time = float(chunk['alternatives'][0]['words'][-1]['endTime'][:-1])
        
        if voices:
            speaker_id = sorted(voice_chunks, key=lambda x: getOverlap(
            [x['start_time'], x['end_time']], [start_time, end_time]), reverse=True)[0]['speaker']

        # if(prev_speaker == speaker_id):
        #     prev_chunk_json = messages[-1]
        #     prev_chunk_json['end_time'] = timedelta(end_time)
        #     prev_chunk_json['text'] += chunk['alternatives'][0]['text']
        #     continue

        chunk_json = {'id': i // 2}
        chunk_json['speaker'] = speaker_id if voices else default_speaker
        chunk_json['text'] = chunk['alternatives'][0]['text']
        chunk_json['start_time'] = str(
            timedelta(seconds=start_time)).split(".")[0]
        chunk_json['end_time'] = str(
            timedelta(seconds=start_time)).split(".")[0]
        #prev_speaker = speaker_id
        messages.append(chunk_json)
        k += 1

    transcript_json['message_list'] = messages
    return transcript_json


# def voice_segmentation(file_path):
#     file_wav = f'{os.path.basename(file_path)}.wav'

#     audio_in = AudioSegment.from_file(file_path)
#     _ = audio_in.export(file_wav, format='wav')
#     diarization = voice_segmentation_pipeline(file_wav)

#     chunks = []
#     for turn, _, speaker in diarization.itertracks(yield_label=True):
#         chunks.append({
#             'start_time': float(turn.start),
#             'end_time': float(turn.end),
#             'speaker': speaker
#         })
#     res_json = {'chunks': chunks}

#     os.remove(file_wav)
#     return res_json
