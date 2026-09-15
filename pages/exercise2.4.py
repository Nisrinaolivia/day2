# ===== IMPORTS: bring in all the tools we need =====
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import chromadb
import re
import os

# ===== SETUP: load the secret key and connect to OpenAI =====
load_dotenv()
client = OpenAI()

# ===== PAGE TITLE =====
st.title("Exercise 2.4 - RAG with Chroma")

SAVE_PATH = "saved_document.txt"

# ===== CONNECT TO CHROMA: open the database on disk, once =====
@st.cache_resource
def get_collection():
    chroma_client = chromadb.PersistentClient(path="./my_chroma_db")
    return chroma_client.get_or_create_collection(name="my_document")


collection = get_collection()

if os.path.exists(SAVE_PATH):
    with open(SAVE_PATH, "r", encoding="utf-8") as f:
        text = f.read()
    st.success("Loaded your saved document.")
else:
    st.warning("No saved document found. Please upload one on the Exercise 2.1 page first.")
    text = None

if text is not None:
     # ===== CHUNK THE DOCUMENT: split the text into groups of sentences =====
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences_per_chunk = st.number_input("Sentences per chunk", min_value=1, value=10)
    chunks = [" ".join(sentences[i:i + sentences_per_chunk]) for i in range(0, len(sentences), sentences_per_chunk)]
    st.write(f"The document was split into {len(chunks)} chunks.")

    # ===== STEP 2 - STORE IN CHROMA: embed the chunks and save them (only the first time) =====
    if collection.count() == 0:
        with st.spinner(f"Embedding {len(chunks)} chunks..."):
            response = client.embeddings.create(
                model="text-embedding-3-large",
                input=chunks,
            )
            embeddings = [item.embedding for item in response.data]

        # Put the chunks and their embeddings into the Chroma database
        collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=[f"chunk_{i}" for i in range(len(chunks))],
        )
        st.success(f"All {len(chunks)} chunks stored in Chroma.")
    else:
        st.info(f"Using {collection.count()} chunks already stored in Chroma.")

 # ===== STEP 3 - ASK A QUESTION: type a question about the document =====
    question = st.text_input("Ask a question about the document:")

    if question:
        question_embedding = client.embeddings.create(
            model="text-embedding-3-large",
            input=question,
        ).data[0].embedding

        # ===== RETRIEVE: ask Chroma for the chunk most similar to the question =====
        results = collection.query(
            query_embeddings=[question_embedding],
            n_results=1,
        )
        best_chunk = results["documents"][0][0]

        # ===== GENERATE: give that chunk to GPT-4o and ask it to answer =====
        answer = client.responses.create(
            model="gpt-4o",
            input=f"""Answer the question using only the information in the context below.
If the answer is not in the context, say so.

Context: {best_chunk}

Question: {question}""",
        )
        
        # ===== SHOW THE ANSWER AND ITS SOURCE =====
        st.write("### Answer")
        st.write(answer.output_text)

        st.write("### Source used from the document")
        st.write(best_chunk)