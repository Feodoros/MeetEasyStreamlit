from UIHelper import streamlit_followup_builder
from Transcriber import assembly_recognition
from Decomposer import decomposition
import streamlit as st
import os
import json

CURRENT_DIR = os.path.dirname(__file__)
DB = os.path.join(CURRENT_DIR, 'DB')
CACHE = os.path.join(CURRENT_DIR, '.cache')

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
            st.info('Transcribing...')  
            meeting_json = assembly_recognition.transcribe_meeting(file_path)
            os.remove(file_path)

            # Decompose meeting:
            # Summary, Tasks, Reminders, plans, etc
            st.info('Decomposing...')
            meeting_json = decomposition.decompose(meeting_json)

            with open(os.path.join(DB, f'{file_name}.json'), 'w+', encoding='utf-8') as f:
                json.dump(meeting_json, f, ensure_ascii=False)

        st.balloons()
        streamlit_followup_builder.build_followup(meeting_json)
