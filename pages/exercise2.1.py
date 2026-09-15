import streamlit as st
from pypdf import PdfReader

st.title("Exercise 2.1")

#1. Allows the user to upload a document.
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        st.write(text)
    else:
        bytes_data = uploaded_file.getvalue()
        string_data = bytes_data.decode("utf-8")
        st.write(string_data)

#2. Allows the user to chunk the document.
    import re

    # Let the user choose how many sentences go in each chunk.
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

    # Show the chunks.
    st.write(f"The document was split into {len(chunks)} chunks.")
    for index, chunk in enumerate(chunks):
        st.write(f"--- Chunk {index + 1} ---")
        st.write(chunk)

 # 3. Show each chunk and let the user choose which ones to save.
    st.write(f"The document was split into {len(chunks)} chunks.")

    # Let the user pick which chunks they want.
    chunk_labels = [f"Chunk {i + 1}" for i in range(len(chunks))]
    selected = st.multiselect(
        "Which chunks do you want to save?",
        chunk_labels,
    )

    # Show every chunk so the user can read them.
    for index, chunk in enumerate(chunks):
        st.write(f"--- Chunk {index + 1} ---")
        st.write(chunk)

    # Combine the selected chunks and offer them as one download.
    if selected:
        chosen_text = ""
        for label in selected:
            number = int(label.replace("Chunk ", ""))   # "Chunk 3" -> 3
            chosen_text += chunks[number - 1] + "\n\n"

        st.download_button(
            label="Save selected chunks",
            data=chosen_text,
            file_name="selected_chunks.txt",
            mime="text/plain",
        )

#4. Read the first chunk you have saved and stores it in a variable.

#5. Displays the first chunk back to the user.

