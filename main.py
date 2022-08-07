import streamlit as st

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    st.write(bytes_data)

if st.button('Process file'):
    if bytes_data:
        print('Done')
