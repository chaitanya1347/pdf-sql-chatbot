from config import S3_BUCKET_NAME,s3,GOOGLE_API_KEY
from templates import pdf_template
from io import BytesIO
from PyPDF2 import PdfReader
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import google.generativeai as genai
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=GOOGLE_API_KEY)
model = ChatGoogleGenerativeAI(model = "gemini-pro",temperature = 0.3)

def get_pdf_text_from_s3(pdf_keys):
    text = ""
    for key in pdf_keys:
        response = s3.get_object(Bucket = S3_BUCKET_NAME,Key = key['Key'])
        file_stream = BytesIO(response['Body'].read())
        
        # Read the PDF file
        pdf_reader = PdfReader(file_stream)  
        for page in pdf_reader.pages:
            text += page.extract_text() or ""  # Append text or an empty string if None
    return text

   
def get_text_chunks(raw_text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size = 2000, chunk_overlap = 200)
    chunks = text_splitter.split_text(raw_text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("Data/faiss_index")
 

def get_conversational_chain():

    prompt = ChatPromptTemplate.from_template(pdf_template)

    document_chain=create_stuff_documents_chain(model,prompt)
    return document_chain

def user_input(user_question):
    embeddings = GoogleGenerativeAIEmbeddings(model = "models/embedding-001")
    
    new_db = FAISS.load_local("Data/faiss_index", embeddings,allow_dangerous_deserialization=True)
    retriever= new_db.as_retriever()
    document_chain = get_conversational_chain()

    retrieval_chain=create_retrieval_chain(retriever,document_chain)
    response=retrieval_chain.invoke({"input":user_question})
    return response['answer']