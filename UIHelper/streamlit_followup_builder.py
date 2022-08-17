import streamlit as st
import os
from datetime import datetime

overall_markdown_str = ''

CURRENT_DIR = os.path.dirname(__file__)


def build_followup(meeting_json):
    global overall_markdown_str

    st.success("Here's your followup!")

    chapters = meeting_json.get('chapters')
    if not chapters:
        st.warning("Possible exception: no chapters")
        return

    overall_summary = ''
    for chapter in chapters:
        overall_summary += chapter['summary'] + ' '

    st.markdown('## Key words:')
    overall_markdown_str += '## Key words:' + '\n'
    key_words = meeting_json['topic']
    for kw in key_words:
        overall_markdown_str += f"- {kw}" + '\n'
        st.markdown(f"- {kw}")

    st.markdown("## Summary:")
    overall_markdown_str += "## Summary:" + '\n'
    st.write(overall_summary)
    overall_markdown_str += overall_summary + '\n'

    st.markdown("## Tasks:")
    overall_markdown_str += "## Tasks:" + '\n'
    tasks = meeting_json['task']
    for task in tasks:
        overall_markdown_str += f"- {task}" + '\n'
        st.markdown(f"- {task}")

    st.markdown("## Chapters:")
    overall_markdown_str += "## Chapters:" + '\n'
    st.markdown(
        """
        <style>
        .streamlit-expanderHeader {
            font-size: 140%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    for chapter in chapters:
        with st.expander(chapter['headline']):
            overall_markdown_str += f"### {chapter['headline']}" + '\n'
            overall_markdown_str += "#### Chapter summary:" + '\n'
            overall_markdown_str += f"{chapter['summary']}" + '\n'
            overall_markdown_str += f"#### Chapter transcript:" + '\n'

            st.markdown("#### Chapter summary:")
            st.markdown(chapter['summary'])
            st.markdown("#### Chapter transcript:")
            message_list_2_markdown(chapter['message_list'])

    st.sidebar.title("Table of contents")
    st.sidebar.markdown('\n'.join([f"<a href='#key-words'>Key words</a>",
                                   "<br>",
                                   f"<a href='#summary'>Summary</a>",
                                   "<br>",
                                   f"<a href='#tasks'>Tasks</a>",
                                   "<br>",
                                   f"<a href='#chapters'>Chapters</a>"]), unsafe_allow_html=True)

    followup_2_pdf()


def message_list_2_markdown(message_list):
    global overall_markdown_str
    for message in message_list:
        colored_text = message['coloured']
        res_text = ''
        k = 0
        for text in colored_text:
            if (k % 2 == 1):
                text = f'<span style="font-size:1.25em;color:#0084b0">{text}</span>'
            k += 1
            res_text += text + ' '

        st.markdown(
            f"{message['start_time']} **{message['speaker']}**: {res_text}", unsafe_allow_html=True)
        overall_markdown_str += f"{message['start_time']} **{message['speaker']}**: {res_text}\\" + '\n'


def followup_2_pdf():
    filename = datetime.now().strftime("followup_%H_%M_%S") + '.md'
    st.download_button(
        label="Download followup",
        data=overall_markdown_str,
        file_name=filename,
        mime='text/csv')
