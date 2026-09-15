# ===== IMPORTS AND SETUP =====
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import numpy as np

load_dotenv()
client = OpenAI()

st.title("Exercise 2.2")

# ===== 1. GET TWO TEXTS FROM THE USER =====
text1 = st.text_area("First text", "It was the best of times...")
text2 = st.text_area("Second text", "In the beginning...")

# ===== 2. EMBED + 3. COMPARE (only when both boxes have text) =====
if text1 and text2:
    # Create an embedding for each text.
    embedding1 = client.embeddings.create(
        model="text-embedding-3-large",
        input=text1,
    ).data[0].embedding

    embedding2 = client.embeddings.create(
        model="text-embedding-3-large",
        input=text2,
    ).data[0].embedding

    # Display the cosine similarity of the two embeddings.
    a = np.array(embedding1)
    b = np.array(embedding2)
    cosine_similarity = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    st.write(f"Cosine similarity: {cosine_similarity}")
else:
    st.info("Enter text in both boxes to see their similarity.")