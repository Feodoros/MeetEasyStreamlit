from UIHelper import streamlit_followup_builder
from Transcriber import assembly_recognition, yandex_transcription
from Decomposer import decomposition
from pydub import AudioSegment
import datetime
import streamlit as st
import os
import json
from markdown import markdown
import pdfkit
import subprocess
from Langdentifier.lang_identification import *


CURRENT_DIR = os.path.dirname(__file__)
DB = os.path.join(CURRENT_DIR, 'DB')
CACHE = os.path.join(CURRENT_DIR, '.cache')

SUPPORTED_AUDIO_TYPES = ['.3ga', '.8svx', '.aac', '.ac3', '.aif', 'aiff', '.alac', '.amr', '.ape', '.au', '.dss',
                         '.flac', '.flv', '.m4a', '.m4b', '.m4p', '.m4r', '.mp3', '.mpga', '.ogg', '.oga', '.mogg',
                         '.opus', '.qcp', '.tta', '.voc', '.wav', '.wma', '.wv']

SUPPORTED_VIDEO_TYPES = ['.webm', '.MTS', '.M2TS',
                         '.TS', '.mov', '.mp2', '.mp4', '.m4p', '.m4v', '.mxf']

SUPPORTED_LANGS = ['en', 'ru']

if not os.path.exists(DB):
    os.mkdir(DB)
if not os.path.exists(CACHE):
    os.mkdir(CACHE)


def main():
    st.set_page_config(page_title="MyMeet · Upload", page_icon="🌿")

    if "meeting_json" not in st.session_state:
        st.session_state.meeting_json = {}

    if "full_markdown" not in st.session_state:
        st.session_state.full_markdown = ''

    with st.expander("How to use", True):
        st.write("1) Upload a recording of your meeting")
        st.write(
            "2) Get a short summary, task list, and full transcript of the meeting")
        st.write("3) Processing time: 30 sec - 15 minutes, depending on file size")

    title = st.text_input('Meeting name', '')
    uploaded_file = st.file_uploader("Choose a recording")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        file_name = uploaded_file.name

        if st.button('Process file'):
            if not bytes_data:
                pass

            # Process file
            with st.spinner('Wait for it...'):
                file_path = os.path.join(CACHE, file_name)
                with open(file_path, 'wb+') as f:
                    f.write(bytes_data)

                _, file_extension = get_file_name_and_ext(file_path)

                # Converting video or unsupported audio to .wav format
                if file_extension not in SUPPORTED_AUDIO_TYPES:
                    st.info("Extracting audio...")
                    file_path = convert_file(file_path)

                duration = get_audio_duration(file_path)
                approximate_time = duration * 0.4
                st.info(
                    f"Approximate processing time: {str(datetime.timedelta(seconds=round(approximate_time)))}")

                st.info('Identifying the language...')
                lang = detect_lang(file_path)
                if lang not in SUPPORTED_LANGS:
                    st.error(f"Unsupported language detected: {lang}")
                    pass
                st.info(f'Detected language: {lang}')

                if lang != 'ru':
                    # Transcribe meeting
                    st.info('Transcribing...')
#                     meeting_json = yandex_transcription.transcribe_meeting(file_path)
                    lang = 'en'

                    try:
                        meeting_json = assembly_recognition.transcribe_meeting(
                            file_path)
                    except Exception as e:
                        message = e
                        if hasattr(e, 'message'):
                            message = e.message
                        st.error(
                            f"Error occurred while transcribing meeting: {message}")
                        pass
                    finally:
                        os.remove(file_path)

                    # Decompose meeting:
                    # Summary, Tasks, Reminders, plans, etc
                    st.info('Decomposing...')
                    meeting_json = decomposition.decompose(meeting_json, lang)

                    meeting_json['file_name'] = file_name
                    meeting_json['title'] = title
                    with open(os.path.join(DB, f"{file_name.split(chr(92))[-1]}.json"), 'w+', encoding='utf-8') as f:
                        json.dump(meeting_json, f, ensure_ascii=False)

                    st.balloons()
                    st.session_state.meeting_json = meeting_json
                else:
                    st.info(
                        'We do not have solution for the Russian language yet, but we are working on it, so please stay tuned!')

    if (st.session_state.meeting_json):
        full_markdown = streamlit_followup_builder.build_followup(
            st.session_state.meeting_json)
        st.session_state.full_markdown = full_markdown
    if (st.session_state.meeting_json and st.session_state.full_markdown):
        download_followup(st.session_state.full_markdown,
                          st.session_state.meeting_json)


def download_followup(full_markdown, meeting_json):
    option = st.selectbox(
        "How would you like to download followup?", ("Markdown", "JSON", "PDF"))

    title = meeting_json.get('title')
    filename = title if title else meeting_json['file_name']

    if option == "Markdown":
        st.download_button(
            label="Download md",
            data=full_markdown,
            file_name=filename + '.md',
            mime='text/csv')
    elif option == "JSON":
        json_str = json.dumps(meeting_json, indent=4)
        st.download_button(
            label="Download json",
            data=json_str,
            file_name=filename + '.json',
            mime='application/json')
    elif option == "PDF":
        html_text = markdown(full_markdown, output_format='html4')
        pdfkit.from_string(html_text, filename + '.pdf')
        with open(filename + '.pdf', "rb") as pdf_file:
            PDFbyte = pdf_file.read()
        st.download_button(
            label="Download pdf",
            data=PDFbyte,
            file_name=filename + '.pdf',
            mime='application/octet-stream')
        os.remove(filename + '.pdf')

    st.markdown("**MeetEasy** - Perfect AI assistant for your meeting.")
    st.markdown("Make your meetings **more productive.**")


def get_audio_duration(file_path):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", file_path],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT)
    return float(result.stdout)


def convert_file(file_path):
    file_name, _ = get_file_name_and_ext(file_path)
    converted_file_path = f"{file_name}.wav"
    subprocess.call(['ffmpeg', '-i', file_path,
                    '-vcodec', 'copy', converted_file_path])
    os.remove(file_path)
    return converted_file_path


def detect_lang(file_path):
    file_name, _ = get_file_name_and_ext(file_path)
    shortened_file_path = f"{file_name}_shortened.wav"
    try:
        subprocess.call(['ffmpeg', '-n', '-i', file_path,
                        '-to', '20', '-vcodec', 'copy', shortened_file_path])
        shortened_read_audio = read_audio(
            shortened_file_path, sampling_rate=SAMPLING_RATE)
        lang = get_language(shortened_read_audio, model)
        return lang
    except:
        return ''
    finally:
        os.remove(shortened_file_path)


def get_file_name_and_ext(file_path):
    return os.path.splitext(file_path)


if __name__ == "__main__":
    main()
