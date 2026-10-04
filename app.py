import logging
import os

import streamlit as st
from dotenv import load_dotenv
from groq import Groq, RateLimitError

load_dotenv()

st.title("My GenAI Assistant")
st.write("Ask a question and get a short answer using Groq.")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("Configure GROQ_API_KEY in .env or Streamlit Secrets.")
    st.stop()

# Avoid automatically retrying requests that hit a rate limit.
client = Groq(api_key=api_key, max_retries=0)

with st.form("question_form"):
    question = st.text_area(
        "Enter your question",
        placeholder="Example: What is generative AI?",
        max_chars=1000,
    )
    submitted = st.form_submit_button("Get Answer")

if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Generating your answer..."):
                response = client.chat.completions.create(
                    model="openai/gpt-oss-20b",
                    max_completion_tokens=512,
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                "You are a helpful teacher. "
                                "Use simple English. "
                                "Keep your answer within 100 words."
                            ),
                        },
                        {
                            "role": "user",
                            "content": question.strip(),
                        },
                    ],
                )

            answer = response.choices[0].message.content

            if answer:
                st.subheader("Answer")
                st.write(answer)
            else:
                st.info(
                    "No answer text was returned within the output "
                    "budget. Try a simpler question."
                )

        except RateLimitError as error:
            retry_after = error.response.headers.get("retry-after")

            if retry_after:
                st.warning(
                    "Groq usage limit reached. "
                    f"Try again after {retry_after} seconds."
                )
            else:
                st.warning(
                    "Groq usage limit reached. Please try again later."
                )

        except Exception:
            logging.exception("Groq request failed")
            st.error("Unable to generate an answer. Please try again.")