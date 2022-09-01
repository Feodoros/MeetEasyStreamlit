from UIHelper import streamlit_followup_builder
from Transcriber import assembly_recognition
from Decomposer import decomposition
from pydub import AudioSegment
import datetime
import streamlit as st
import os
import json
from markdown import markdown
import pdfkit


CURRENT_DIR = os.path.dirname(__file__)
DB = os.path.join(CURRENT_DIR, 'DB')
CACHE = os.path.join(CURRENT_DIR, '.cache')

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
        st.write("2) Get a short summary, task list, and full transcript of the meeting")
        st.write("3) Processing time: 30 sec - 15 minutes, depending on file size")

    uploaded_file = st.file_uploader("Choose a file")
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        file_name = uploaded_file.name

        if st.button('Process file'):
            if bytes_data:
                file_path = os.path.join(CACHE, file_name)
                with open(file_path, 'wb+') as f:
                    f.write(bytes_data)

            with st.spinner('Wait for it...'):
                audio = AudioSegment.from_file(file_path)
                duration = audio.duration_seconds
                approximate_time = duration * 0.4
                st.info(
                    f"Approximate processing time: {str(datetime.timedelta(seconds=round(approximate_time)))}")
                st.info('Transcribing...')
                meeting_json = assembly_recognition.transcribe_meeting(
                    file_path)
                os.remove(file_path)

                # Decompose meeting:
                # Summary, Tasks, Reminders, plans, etc
                st.info('Decomposing...')
                meeting_json = decomposition.decompose(meeting_json)

                with open(os.path.join(DB, f'{file_name}.json'), 'w+', encoding='utf-8') as f:
                    json.dump(meeting_json, f, ensure_ascii=False)
            meeting_json['file_name'] = file_name
            st.balloons()
            st.session_state.meeting_json = meeting_json

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

    filename = meeting_json['file_name']
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


if __name__ == "__main__":
    main()
