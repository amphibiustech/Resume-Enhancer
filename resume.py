import streamlit as st
import logging
logging.basicConfig(level=logging.WARN,
                    filename="logs.log",
                    filemode="a",
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S")
import os 
import warnings
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



def home():

    st.set_page_config("Resume Enhancer | Amphibius",
                       page_icon="chart_with_upwards_trend",)
    st.title("RAG based Resume Enhancer Using GenAI capabilities 	:white_check_mark:")
    
    prompt = PromptTemplate.from_template('''You need to act as an Resume Enhancer or Resume Writer based on user {requirement}, 
                                          Kindly help job seekers are per there need in well generated , relevant content and in resume format
                                          also take the reference of {resume}.
                                          If you're not able to answer properly then just say ask another requirement ! ''')
    
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
                
                with open("resume.txt","w") as f:
                    file = f.write(result.text)
                    
                st.download_button("File_Download",data=result.text,file_name="resume1.txt")
                st.success("Done")


    
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

