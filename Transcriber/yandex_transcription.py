import boto3
import secrets
import os
from Transcriber import utils


# Saving to cloud keys
# https://cloud.yandex.com/en-ru/docs/speechkit/stt/transcribation#examples_ogg
AWS_KEY_ID = 'YCAJEwNca6xrC9GwBcFRhdNys'  # service account key_id
AWS_KEY_VALUE = 'YCO0hXawJLhOXmYOVux-K-6MQaIdMvYt17VLjFq-'  # service account secret
AWS_CLIENT = boto3.client(
    service_name='s3',
    aws_access_key_id=AWS_KEY_ID,
    aws_secret_access_key=AWS_KEY_VALUE,
    endpoint_url='https://storage.yandexcloud.net'
)
# Speech recognition keys
# for more info check: https://cloud.yandex.ru/docs/storage/tools/boto
# https://cloud.yandex.ru/docs/iam/operations/sa/create-access-key
BUCKET_NAME = 'meet-easy'
API_KEY = 'AQVNzYho0g2FuMbWorhKIBZ9HqSxBq-O_ue7oRZr'  # api key
POST = "https://transcribe.api.cloud.yandex.net/speech/stt/v2/longRunningRecognize"


def transcribe_meeting(recording_path):
    transcript_json = get_transcript(
        recording_path, AWS_CLIENT, BUCKET_NAME, API_KEY, POST)
    return transcript_json


def get_transcript(mp3_path, aws_client, bucket_name, api_key, post):
    new_name = secrets.token_hex(16) + '.ogg'
    load_response = utils.load_mp3_to_bucket(
        mp3_path, new_name, aws_client, bucket_name)

    if load_response['HTTPStatusCode'] == 200:
        print('File was loaded to Yandex Storage')
        print('Getting transcriprt...')

        transcript_response = utils.get_audio_recognition(
            new_name, api_key, post, bucket_name)
        os.remove(new_name)

        if 'error' in transcript_response.keys():
            error = transcript_response['error']['message']
            print(f'Transcribing was failed with error: {error}')

        voice = False
        if voice:
            print('Voice segmentation...')
            voice_time_json = utils.voice_segmentation(mp3_path)
        else:
            voice_time_json = {}

        print('Started to convert it to the right format')
        return utils.transcript_to_json(transcript_response, voice_time_json)
    else:
        return {'error': {'type': 'load error', 'message': load_response['Error']}}
