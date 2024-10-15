from fastapi import FastAPI, HTTPException, Depends, File, UploadFile
from src.Insertion import storing_in_db, initialize_weaviate, embedd_model
from src.retriever_and_generator import create_prompts, retriever_and_LLM_Generation
from langchain.prompts import ChatPromptTemplate
from langchain import HuggingFaceHub
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel
from typing import List
import os
import weaviate

load_dotenv()

# Folder to save the uploaded files
UPLOAD_FOLDER = "Uploaded_files"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app = FastAPI()
file_details = []

# Initialize Weaviate client and embedding model
client = initialize_weaviate()
embedder = embedd_model()

# Model for query requests
class QueryRequest(BaseModel):
    query: str

class FileName(BaseModel):
    file_name: str




# File upload endpoint to process documents
@app.post('/process_documents/')
async def process_documents(files: List[UploadFile] = File(...)):
    for file in files:
        file_name = file.filename
        file_location = os.path.join(UPLOAD_FOLDER, file_name)

        # Save the file locally
        with open(file_location, 'wb') as f:
            f.write(await file.read())

        # Store file details
        file_details.append(file_name)

    # Return the list of file details
    return {"files": file_details}

# Retrieve the list of uploaded files
@app.get('/files_uploaded/')
async def files_uploaded():
    return {"files": file_details}

# Ingest documents into the vector database

@app.post('/ingestion')
async def ingestion(file_names: List[str]):
    for file_name in file_names:
        file_location = os.path.join(UPLOAD_FOLDER, file_name)
        if not os.path.exists(file_location):
            raise HTTPException(status_code=404, detail=f"File {file_location} does not exist.")
    
    try:
        # Store documents in vector DB
        vector_db = storing_in_db(file_names, client, embedder)
        app.state.vector_db = vector_db  # Store vector DB in app state
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    # Return only necessary information
    return {
        'status': 'success',
        'file_names': file_names,
        'message': 'Files successfully ingested'
    }












# Dependency to retrieve the stored vector_db from app state
async def get_vector_db(app: FastAPI = Depends(lambda: app)):
    if not hasattr(app.state, "vector_db"):
        raise ValueError("Vector DB not initialized.")
    return app.state.vector_db













# Endpoint for querying the RAG system
@app.post('/rag')
async def query_rag_system(request: QueryRequest, vector_db: str = Depends(get_vector_db)):
    query = request.query
    prompt = create_prompts()  # Ensure this function is properly defined
    answer  , context = retriever_and_LLM_Generation(vector_db, prompt, query)  # Ensure this function is defined
    context = context.replace('\n' , ' ')
    return {'response': answer , 'metadata' : context}




if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
