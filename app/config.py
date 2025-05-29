import streamlit as st
import os
from langchain.chat_models import init_chat_model
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS


# --- Setup LLM ---
@st.cache_resource
def initialize_llm():
    os.environ["TOGETHER_API_KEY"] = "0615fdd7532c37911dbfc20bfe57bd0cc04035cd713adff2a2993d80bd5bb0ed"
    return init_chat_model("mistralai/Mixtral-8x7B-Instruct-v0.1", model_provider="together")

llm = initialize_llm()


# --- RAG Setup ---
@st.cache_resource
def setup_rag():
    # Load PDF
    file_path = "Weather Activity Clothing Database.pdf"
    loader = PyPDFLoader(file_path)
    documents = loader.load()

    # Split into chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    faiss_db = FAISS.from_documents(chunks, embedding_model)
    faiss_db.save_local("rag_faiss_index")
    faiss_db = FAISS.load_local("rag_faiss_index", embedding_model, allow_dangerous_deserialization=True)
    return faiss_db.as_retriever()