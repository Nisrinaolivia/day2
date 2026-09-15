import streamlit as st
from pypdf import PdfReader
import re
import os
import shutil

st.title("Exercise 2.1")

SAVE_PATH = "saved_document.txt"

# --- Load the document: either from a new upload, or from the saved file ---
text = None

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    # A new file was uploaded — read it and save it to disk.
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        text = uploaded_file.getvalue().decode("utf-8")

    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    st.success("Document uploaded and saved.")

elif os.path.exists(SAVE_PATH):
    # No new upload, but a saved document exists — load it.
    with open(SAVE_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    st.info("Loaded your previously saved document.")


# --- Only continue if we have a document ---
if text is not None:
    # Choose how many sentences per chunk.
    sentences_per_chunk = st.number_input(
        "How many sentences per chunk?",
        min_value=1,
        value=3,
    )

    # Split the text into sentences, then group them into chunks.
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    for i in range(0, len(sentences), sentences_per_chunk):
        group = sentences[i:i + sentences_per_chunk]
        chunks.append(" ".join(group))

    st.write(f"The document was split into {len(chunks)} chunks.")

    # Show the chunks on the page.
    with st.expander("View all chunks"):
        for index, chunk in enumerate(chunks):
            st.write(f"**Chunk {index + 1}**")
            st.write(chunk)

    # Save each chunk as its own file in a "chunks" folder (visible in Explorer).
    if os.path.exists("chunks"):
        shutil.rmtree("chunks")
    os.makedirs("chunks", exist_ok=True)

    for index, chunk in enumerate(chunks):
        chunk_path = f"chunks/chunk_{index + 1}.txt"
        with open(chunk_path, "w", encoding="utf-8") as f:
            f.write(chunk)

    st.success(f"Saved {len(chunks)} chunks to the 'chunks' folder.")