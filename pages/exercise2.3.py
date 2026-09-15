import streamlit as st
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np
import re
import os

load_dotenv()
client = OpenAI()

st.title("Exercise 2.3 - Manual RAG")

SAVE_PATH = "saved_document.txt"


def get_embedding(text):
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=text,
    )
    return np.array(response.data[0].embedding)


def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


# --- Load the document: either from a new upload, or from the saved file ---
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


# --- Only continue if we have a document ---
if text is not None:
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

    with st.expander("View all chunks"):
        for index, chunk in enumerate(chunks):
            st.write(f"**Chunk {index + 1}**")
            st.write(chunk)

    # --- Ask a question ---
    question = st.text_input("Ask a question about the document:")

    if question:
        question_embedding = get_embedding(question)

        best_score = -1
        best_chunk = ""
        for chunk in chunks:
            chunk_embedding = get_embedding(chunk)
            score = cosine_similarity(question_embedding, chunk_embedding)
            if score > best_score:
                best_score = score
                best_chunk = chunk

        response = client.responses.create(
            model="gpt-4o",
            input=f"""Answer the question using only the information in the context below.
If the answer is not in the context, say so.

Context: {best_chunk}

Question: {question}""",
        )

        st.write("### Answer")
        st.write(response.output_text)

        best_index = chunks.index(best_chunk)
        st.write("### Source used from the document")
        st.write(f"This answer came from **Chunk {best_index + 1}** (match score: {best_score:.2f})")
        st.write(best_chunk)