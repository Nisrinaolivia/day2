# ===== IMPORTS =====
import streamlit as st
from pypdf import PdfReader
import re
import os
import shutil

st.title("Exercise 2.1")

SAVE_PATH = "saved_document.txt"

# ===== 1. UPLOAD: load a new document, or the previously saved one =====
text = None
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
    else:
        text = uploaded_file.getvalue().decode("utf-8")

    with open(SAVE_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    st.success("Document uploaded and saved.")

elif os.path.exists(SAVE_PATH):
    with open(SAVE_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    st.info("Loaded your previously saved document.")


if text is not None:
    # ===== 2. CHUNK: split the document into groups of sentences =====
    sentences_per_chunk = st.number_input(
        "How many sentences per chunk?",
        min_value=1,
        value=3,
    )
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

    # ===== 3. SAVE: write each chunk as its own file in the "chunks" folder =====
    if os.path.exists("chunks"):
        shutil.rmtree("chunks")
    os.makedirs("chunks", exist_ok=True)

    for index, chunk in enumerate(chunks):
        chunk_path = f"chunks/chunk_{index + 1:03d}.txt"
        with open(chunk_path, "w", encoding="utf-8") as f:
            f.write(chunk)

    st.success(f"Saved {len(chunks)} chunks to the 'chunks' folder.")

    # ===== 4. READ BACK: read the first saved chunk and display it =====
    first_chunk_path = "chunks/chunk_001.txt"
    if os.path.exists(first_chunk_path):
        with open(first_chunk_path, "r", encoding="utf-8") as f:
            first_chunk = f.read()

        st.subheader("First saved chunk (read back from disk)")
        st.write(first_chunk)