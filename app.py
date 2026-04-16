import streamlit as st
from groq import Groq

import os
client = Groq(api_key=os.environ["GROQ_API_KEY"])

st.title("AI Product Insight Tool")

st.write("Enter customer reviews and get AI-powered insights.")

reviews = st.text_area("Paste reviews (one per line):")

if st.button("Analyze"):

    if not reviews.strip():
        st.warning("Please enter some reviews first.")
    else:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {
                    "role": "user",
                    "content": f"""
You are a product analyst.

Analyze these customer reviews:

{reviews}

Return:
1. Top complaints
2. Top positives
3. 3 product improvement ideas
"""
                }
            ]
        )

        st.subheader("AI Analysis")
        st.write(response.choices[0].message.content)