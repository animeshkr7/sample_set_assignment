from typing import List
import weaviate
import os
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Weaviate

# Initialize Weaviate client
def initialize_weaviate():
    load_dotenv()

    WEAVIATE_URL = os.getenv("WEAVIATE_CLUSTER")
    WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY")

    client = weaviate.Client(
        url=WEAVIATE_URL, auth_client_secret=weaviate.AuthApiKey(WEAVIATE_API_KEY)
    )

    return client

# Initialize embedding model
def embedd_model():
    embedding_model_name = 'Sentence-Transformers/all-mpnet-base-v2'
    embedding_model = HuggingFaceEmbeddings(model_name=embedding_model_name)
    return embedding_model

# Load a PDF and return its pages
def load_pdf(file_name):
    path = 'Uploaded_files/'  # Directory where the files are uploaded
    path = os.path.join(path, file_name)

    if not os.path.exists(path):
        raise FileNotFoundError(f"The file {path} does not exist.")

    loader = PyPDFLoader(path)
    pages = loader.load()

    return pages

# Create document chunks for vector storage
def create_chunks(pages):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=50)
    docs = text_splitter.split_documents(pages)
    return docs

# Store multiple documents in vector DB, reusing client and embedder
def storing_in_db(file_names: List[str], client, embedder):
    all_docs = []

    for file_name in file_names:
        pages = load_pdf(file_name)  # Load the PDF file
        docs = create_chunks(pages)  # Create chunks from the PDF
        all_docs.extend(docs)  # Collect all document chunks

    # Store all documents in Weaviate (can be done once after processing all docs)
    vector_db = Weaviate.from_documents(
        all_docs,
        embedder,
        client=client,
        by_text=False
    )

    return vector_db
