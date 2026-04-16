import streamlit as st
from groq import Groq

from fpdf import FPDF

def create_pdf(text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in text.split("\n"):
        pdf.multi_cell(0, 8, line)

    return pdf.output(dest="S").encode("latin-1")

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

analysis_text = response.choices[0].message.content

st.subheader("📊 AI Analysis")
st.markdown(analysis_text)

pdf = create_pdf(analysis_text)

st.download_button(
    label="📥 Download Report as PDF",
    data=pdf,
    file_name="ai_product_report.pdf",
    mime="application/pdf"
)
