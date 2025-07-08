from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import io
import base64
from PIL import Image
from fpdf import FPDF
import pdf2image
import google.generativeai as genai
import html

# Configure Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Get Gemini response
def get_gemini_response(input, pdf_content, prompt):
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input, pdf_content[0], prompt])
    return response.text  # ✅ Return only the response text for clean output

# Convert PDF to image bytes
def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert the PDF to image (first page only)
        images = pdf2image.convert_from_bytes(
            uploaded_file.read(),
            poppler_path=r"C:\Program Files\Poppler\Library\bin"  
        )

        first_page = images[0]

        # Convert to JPEG byte stream
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        # Return as vision input for Gemini
        pdf_parts = [{
            "mime_type": "image/jpeg",
            "data": base64.b64encode(img_byte_arr).decode()
        }]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

# Streamlit UI
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Resume Analyzer")

input_text = st.text_area("Paste the Job Description:", key="input")
uploaded_file = st.file_uploader("Upload your Resume (PDF only):", type=["pdf"])

if uploaded_file is not None:
    st.success("✅ Resume uploaded successfully!")

# Buttons
submit1 = st.button("📋 Tell Me About the Resume")
submit3 = st.button("📊 Percentage Match")
submit4 = st.button("📝 Generate Optimized Resume")
# Prompts
input_prompt1 = """
You are an experienced Human Resource Manager with Tech Experience in roles such as Data Science, Full Stack, Web Development, Big Data Engineering, DEVOPS, or Data Analyst.
Your task is to review the resume against the provided job description. 
Give a professional evaluation highlighting strengths and weaknesses relevant to the job description.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) with deep understanding of roles like Data Science, Full Stack, Web Development, Big Data Engineering, DEVOPS, or Data Analyst.
Evaluate the resume against the job description and return:
1. Percentage Match
2. Missing Keywords
3. Final Thoughts
"""

input_prompt4 = """
You are a professional resume writer. Based on the candidate's existing resume (image input) and the provided job description (text),
generate a fresh resume that:
- Keeps existing experience and education
- Adds missing keywords relevant to the job description
- Presents the content in a professional resume format

Start with the candidate's name, contact info, then objective, skills, education, projects, and experience.
Keep it concise and relevant to the job description.
"""


#  Resume Evaluation
if submit1:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1, pdf_content, input_text)
        st.subheader("🔎 Evaluation Result:")
        st.write(response)
    else:
        st.warning("⚠️ Please upload your resume first.")

elif submit3:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt3, pdf_content, input_text)
        st.subheader("📊 Percentage Match Result:")
        st.write(response)
    else:
        st.warning("⚠️ Please upload your resume first.")

elif submit4:
    if uploaded_file:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4, pdf_content, input_text)

        st.subheader("📝 Optimized Resume Text:")
        st.write(response)

        # Clean the text for PDF
        cleaned_response = html.unescape(response)
        cleaned_response = cleaned_response.encode('latin-1', errors='ignore').decode('latin-1')

        #  Create PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.set_font("Arial", size=12)

        for line in cleaned_response.split('\n'):
            pdf.multi_cell(0, 10, line)

        #  Convert to byte stream
        pdf_bytes = pdf.output(dest='S').encode('latin-1')

        # Streamlit download button
        st.download_button(
            label="📥 Download Resume as PDF",
            data=pdf_bytes,
            file_name="optimized_resume.pdf",
            mime="application/pdf"
        )
    else:
        st.warning("⚠️ Please upload your resume first.")

