# Importing required libraries
import streamlit as st  # For creating a web-based user interface
import google.generativeai as genai  # For interacting with Google's Generative AI models
import os  # For accessing environment variables
import PyPDF2 as pdf  # For extracting text from PDF files
from dotenv import load_dotenv  # For loading environment variables from a .env file
import json  # For handling JSON data

# Load environment variables from a .env file
load_dotenv()  # This is essential to securely store and retrieve sensitive data like API keys

# Configure Google Generative AI with an API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to interact with the Gemini AI model
def get_gemini_repsonse(input):
    model = genai.GenerativeModel('gemini-pro')  # Instantiate the Gemini AI model
    response = model.generate_content(input)  # Generate a response based on the input prompt
    return response.text  # Return the AI-generated text response

# Function to extract text from an uploaded PDF file
def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)  # Read the uploaded PDF file
    text = ""  # Initialize an empty string to store the extracted text
    for page in range(len(reader.pages)):  # Loop through all the pages in the PDF
        page = reader.pages[page]  # Get the current page
        text += str(page.extract_text())  # Extract text from the page and append it
    return text  # Return the concatenated text from all pages

# Prompt template for interacting with the AI model
input_prompt = """
Hey Act Like a skilled or very experienced ATS(Application Tracking System)
with a deep understanding of tech field, software engineering, data science, data analyst,
and big data engineering. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive, and you should provide 
the best assistance for improving the resumes. Assign the percentage matching based 
on the JD and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

# Streamlit App Interface
st.title("Smart ATS")  # Title of the Streamlit application
st.text("Improve Your Resume ATS")  # Short description or tagline

# Text area for pasting the job description
jd = st.text_area("Paste the Job Description")  

# File uploader for uploading the resume in PDF format
uploaded_file = st.file_uploader("Upload Your Resume", type="pdf", help="Please upload the PDF")

# Button for submitting the form
submit = st.button("Submit")

# If the submit button is clicked
if submit:
    if uploaded_file is not None:  # Check if a file is uploaded
        text = input_pdf_text(uploaded_file)  # Extract text from the uploaded PDF
        response = get_gemini_repsonse(input_prompt)  # Get the response from the AI model
        st.subheader(response)  # Display the response as a subheader
