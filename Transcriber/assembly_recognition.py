import requests
import secrets
import os
import time
import random
from datetime import timedelta
import streamlit as st

endpoint = "https://api.assemblyai.com/v2/transcript"

auth_tokens = ["98d634acce314757909483d17a791819", '82532fe8a1f643d6b35ae07fb86aadee', '423b657d17554cf4ad218e4f127e2aae',
               '85948795b8174fea8b565f3934508d2f', '8309e4e43e8d47eb9b787545444dd360', '072eedb31d8146e49c21534a73ce8779',
               'b3ce06ef416c481f9651ab313c9d58ce', 'ce882c6a139b4419b1c799377428ec3a', '75be7ab4f09b4d01b2abd10d04f20b6e',
               'da03de683f59456ba7fe4045231a0d5f', 'd6c350ea98aa4f0b842921bb94ddcda0', '16915072ecb24b9c8b192070cdb8d37b',
               'cca3d5a8062b4164a1d4d6c67b65ee10', '6db1619538f64cfa81f661b702660141', 'fa6576b341724766b3e48c02730d6160']


def post_audio(recording_path):
    # Upload file to server
    headers = get_headers()
    status_code = 500
    while status_code != 200:
        response = requests.post('https://api.assemblyai.com/v2/upload',
                                 headers=headers,
                                 data=read_file_by_chunk(recording_path))
        status_code = response.status_code

        if(status_code != 200):
            auth_tokens.remove(headers['authorization'])
            headers = get_headers()

    response_json = response.json()
    json = {"audio_url": response_json['upload_url'], "speaker_labels": True,
            'auto_chapters': True, "auto_highlights": True, "language_detection": True}
    response = requests.post(endpoint, json=json, headers=headers)

    print('Transcribing...')
    status = 'submitted'
    while status != 'completed':
        print(status)
        polling_response = requests.get(
            endpoint+'/'+response.json()['id'], headers=headers)
        status = polling_response.json()['status']

        if status == 'completed':
            print('Transcribing done.')

        elif status == 'error':

            if polling_response.json()['error'] == "Insufficient Funds":

                auth_tokens.remove(headers['authorization'])

                headers = get_headers()
                polling_response = post_audio(headers, recording_path)
            else:
                print('Transcribing failed with the {} error.'.format(
                    polling_response.json()['error']))

        time.sleep(3)

    return polling_response


def get_headers():
    return {
        "authorization": random.choice(auth_tokens),
        "content-type": "application/json",
        "User-Agent": "Mozilla/5.0"
    }


def transcribe_meeting(recording_path):
    print('Uploading file to cloud')
    polling_response = post_audio(recording_path)
#     response = requests.post('https://api.assemblyai.com/v2/upload',
#                              headers=headers,
#                              data=read_file_by_chunk(recording_path))

#     json = {"audio_url": response.json()['upload_url'], "speaker_labels": True,
#             'auto_chapters': True, "auto_highlights": True, "entity_detection": True}
#     response = requests.post(endpoint, json=json, headers=headers)

#     print('Transcribing...')
#     status = 'submitted'
#     while status != 'completed':
#         print(status)
#         polling_response = requests.get(
#             endpoint+'/'+response.json()['id'], headers=headers)
#         status = polling_response.json()['status']

#         if status == 'completed':
#             print('Transcribing done.')

#         elif status == 'error':

#             if polling_response.json()['status']=="Insufficient Funds":

#                 auth_tokens.remove(headers['authorization'])

#                 headers = {"authorization": random.choice(auth_tokens), "content-type": "application/json"}

#                 pass

#         time.sleep(3)

    return process_transcript_json(polling_response.json())
# def transcribe_meeting(recording_path):
#     new_name = ''
#     filename, file_extension = os.path.splitext(recording_path)
#     if (file_extension not in suported_file_types):
#         print('Convert file to ogg format')
#         new_name = secrets.token_hex(16) + '.ogg'
#         audio_in = AudioSegment.from_file(recording_path)
#         audio_in.export(new_name, format='ogg', codec='libopus')
#         recording_path = new_name

#     print('Uploading file to cloud')
#     response = requests.post('https://api.assemblyai.com/v2/upload',
#                              headers=headers,
#                              data=read_file_by_chunk(recording_path))

#     json = {"audio_url": response.json()['upload_url'], "speaker_labels": True,
#             'auto_chapters': True, "auto_highlights": True, "entity_detection": True}
#     response = requests.post(endpoint, json=json, headers=headers)

#     print('Transcribing...')
#     status = 'submitted'
#     while status != 'completed':
#         print(status)
#         polling_response = requests.get(
#             endpoint+'/'+response.json()['id'], headers=headers)
#         status = polling_response.json()['status']

#         if status == 'completed':
#             print('Transcribing done.')

#         elif status == 'error':

#             if polling_response.json()['status']=="Insufficient Funds":

#                 auth_tokens.remove(headers['authorization'])

#                 headers = {"authorization": random.choice(auth_tokens), "content-type": "application/json"}

#                 pass

#         time.sleep(3)

#     if (new_name):
#         os.remove(new_name)

#     return process_transcript_json(polling_response.json())


def process_transcript_json(resp_json):
    message_list = []
    current_phrase = ''
    id = 0
    start_time = -1

    for word in resp_json['words']:
        if start_time == -1:
            start_time = word['start']

        speaker = word['speaker']
        text = word['text']
        current_phrase += text + ' '
        if text.endswith(('.', '?', '!')):
            message_list.append({
                'id': id,
                'speaker': speaker,
                'text': current_phrase,
                'start_time': str(timedelta(milliseconds=start_time)).split(".")[0],
                'end_time': str(timedelta(milliseconds=word['end'])).split(".")[0]})
            start_time = -1
            id += 1
            current_phrase = ''

    resp_json['message_list'] = message_list
    return resp_json


def read_file_by_chunk(file_path, chunk_size=5242880):
    with open(file_path, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data
