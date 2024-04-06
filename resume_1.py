import streamlit as st
import logging
logging.basicConfig(level=logging.WARN,
                    filename="logs.log",
                    filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
import os 
from PyPDF2 import PdfWriter
import warnings
from fpdf import FPDF

from langchain_community.embeddings import HuggingFaceEmbeddings
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from dotenv import load_dotenv
warnings.filterwarnings('ignore')
import google.generativeai as genai
from langchain_community.vectorstores import FAISS 
from langchain_core.prompts import ChatMessagePromptTemplate,PromptTemplate
import io
load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_pdf_reader(pdf_file):
    text = ''
    with io.BytesIO(pdf_file.read()) as file:
        reader = PdfReader(file)
        for page_num in range(len(reader.pages)) :
            page = reader.pages[page_num]
            text += page.extract_text()
    return text

def create_pdf(file_name,text):
    # Create instance of FPDF class
    pdf = FPDF()

    # Add a page
    pdf.add_page()


    # Add text to the PDF
    # Add text to the PDF
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, txt=text)


    # Save the PDF
    pdf.output(file_name)   

def home():

    st.set_page_config("Resume Enhancer | Amphibius",
                       page_icon="chart_with_upwards_trend",)
    st.title("RAG based Resume Enhancer Using GenAI capabilities 	:white_check_mark:")
    
    prompt = PromptTemplate.from_template('''Enhance the content of the existing {resume}. 
                                          Add detailed descriptions to each job role, emphasizing key achievements and responsibilities.
                                          Ensure the language used is professional and tailored to highlight the candidate's skills, 
                                          education, strengths, career objectives, and experiences effectively. Additionally, 
                                          address the specific {requirement} mentioned in the question to provide comprehensive 
                                          enhancements.''')
    
    file = st.file_uploader("Upload your resume here :")
    
    question = st.text_input("Ask a question or enhance your resume :grey_question:")
    

    
    if st.button("Submit"):
        
        if file is None or question.strip() == "":
            st.warning("Please upload a resume file and provide a question.")
            logging.warn("No file found")
        else:
            with st.spinner("Processing..."):
                raw_text =get_pdf_reader(file)
                ask = prompt.format(requirement=question,resume=raw_text)
                model = genai.GenerativeModel("gemini-pro")
                result = model.generate_content(ask)
                # result = get_resume_enhancer(ask)s
                st.write(result.text)
                
                # Define the file name for the PDF
                file_name = "output.pdf"

                # Call the function to create the PDF
                create_pdf(file_name, result.text)

                # Create a download button
                st.download_button(label="Download PDF", data=open(file_name, "rb").read(), file_name=file_name)


    
    with st.sidebar:
        
        st.header("Used Libraries :")
        
        st.markdown("-**Langchain**")
        st.markdown("-**Gemini-Pro**")
        st.markdown("-**Streamlit**")
        st.markdown("-**Gemini-Pro**")
        st.markdown("-**PyPDF2**")
        
        st.markdown("---")
        st.markdown("This application is developed by **@Amphibius Tech** 2024-25. For more information, write us amphibiustech@gmail.com")
        
        
        
        
                    

        


if __name__ == "__main__":
    home()

