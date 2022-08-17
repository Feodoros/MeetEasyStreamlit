import json
import os
import streamlit_followup_builder

DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(DIR, 'data')

test_followup = os.path.join(DATA_DIR, 'English_0.wav.json')

if __name__ == '__main__':
    with open(test_followup, encoding='utf-8') as f:
        meeting_json = json.load(f)
        
    streamlit_followup_builder.build_followup(meeting_json)