import streamlit as st
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq

from langchain_community.embeddings import HuggingFaceEmbeddings 

from langchain_community.vectorstores import FAISS
from langchain_classic.chains.question_answering import load_qa_chain

from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL_ID = "meta-llama/Llama-3.3-70B-Instruct-Turbo" 


if not GROQ_API_KEY:
    st.error("Error: GROQ AI API key not found.")
    st.info("Please create a .env file in your project directory with GROQ_API_KEY=\"sk-tg-YOUR_ACTUAL_GROQ_AI_TOKEN_HERE\".")
    st.stop() 


st.header("My first Chatbot")


with st.sidebar:
    st.title("Your Documents")
    file = st.file_uploader("Upload a PDF file and start asking questions", type="pdf")


if file is not None:
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()

    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size=500,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    vector_store = FAISS.from_texts(chunks, embeddings)

    user_question = st.text_input("Type Your question here")

    if user_question:
        match = vector_store.similarity_search(user_question)

        llm = ChatGroq(
            model_name='llama-3.1-8b-instant', 
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.1,
            max_tokens=500 
        )

        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents = match, question = user_question)
        st.write(response)