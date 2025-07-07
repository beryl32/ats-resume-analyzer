 🧠 ATS Resume Analyzer using Google Gemini + Streamlit

This is an AI-powered Resume Analyzer and Optimizer built with **Google Gemini 1.5 Flash** and **Streamlit**. It helps job seekers tailor their resumes to job descriptions by simulating how an Applicant Tracking System (ATS) would evaluate resumes.

✨ Features

✅ Upload your resume (PDF format)  
✅ Paste a job description  
✅ Get a professional evaluation of your resume  
✅ See match percentage + missing keywords  
✅ Generate an optimized, ATS-friendly resume  
✅ Download the new resume as a PDF

 🛠 Tech Stack

- Python 3.9+
- Streamlit
- Google Generative AI SDK (`google-generativeai`)
- `pdf2image`, `Pillow`, `fpdf`, `base64`
- `python-dotenv` for environment variable handling

🚀 How to Run Locally
 1. Clone the Repository
git clone https://github.com/beryl32/ats-resume-analyzer.git
cd ats-resume-analyzer

2. Install Dependencies
pip install -r requirements.txt

3. Add Your Gemini API Key
Create a .env file in the root directory and paste your API key:
GOOGLE_API_KEY=your_gemini_api_key_here

4. Run the Streamlit App
streamlit run app.py


🧠 How It Works
The user uploads a PDF resume.

The app converts the first page to an image using pdf2image.

The image is encoded to Base64 and sent along with a job description to Google Gemini.

Gemini analyzes the resume:

Evaluates it

Matches it against job description

Suggests improvements

The user can download a professionally rewritten resume as a PDF.


🔒 Important Notes
Only the first page of the PDF is currently analyzed.
The app requires Poppler for PDF-to-image conversion (on Windows).


