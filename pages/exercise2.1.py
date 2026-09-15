import streamlit as st
from pypdf import PdfReader
import re

st.title("Exercise 2.1")

# 1. Allows the user to upload a document.
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        bytes_data = uploaded_file.getvalue()
        text = bytes_data.decode("utf-8")

    # 2. Allows the user to chunk the document.
    sentences_per_chunk = st.number_input(
        "How many sentences per chunk?",
        min_value=1,
        value=3,
    )

    # Split the text into individual sentences.
    sentences = re.split(r'(?<=[.!?])\s+', text)

    # Group the sentences into chunks.
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        group = sentences[i:i + sentences_per_chunk]
        chunk = " ".join(group)
        chunks.append(chunk)

    # 3. Show a button per chunk that selects it.
    st.write(f"The document was split into {len(chunks)} chunks.")

    for index, chunk in enumerate(chunks):
        if st.button(f"Select Chunk {index + 1}", key=f"select_{index}"):
            st.session_state.selected_chunk = chunk

    # 4. Read the selected chunk and store it in a variable.
    # 5. Display the selected chunk back to the user.
    if "selected_chunk" in st.session_state:
        st.write("--- Selected chunk ---")
        st.write(st.session_state.selected_chunk)