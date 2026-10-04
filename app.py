import os
import logging
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

st.title("My GenAI Assistant")
st.write("Ask a question and get an answer using Groq.")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Add GROQ_API_KEY to your .env file.")
    st.stop()

client = Groq(api_key=api_key)

# Collect the question from the UI.
question = st.text_area(
    "Enter your question",
    placeholder="Example: What is generative AI?",
)

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Generating your answer..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful teacher. "
                                "Explain concepts in simple English."
                            ),
                        },
                        {
                            "role": "user",
                            "content": question,
                        },
                    ],
                )

            st.subheader("Answer")
            st.write(response.choices[0].message.content)

        except Exception:
            logging.exception("Groq request failed")
            st.error("Unable to generate an answer. Please try again.")