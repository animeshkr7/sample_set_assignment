# streamlit_app.py (Streamlit frontend)
import streamlit as st
import requests

# Backend API endpoint
backend_url = "http://127.0.0.1:8000/process_documents/"
files_uploaded_url = "http://127.0.0.1:8000/files_uploaded/" 
ingestion_url = 'http://127.0.0.1:8000/ingestion/'
RAG_URL = 'http://127.0.0.1:8000/rag/' 



# Streamlit app for multiple file uploads with a button
st.title("Document Upload and Processing")

# File uploader allows multiple file selection
uploaded_files = st.file_uploader("Choose multiple documents...", type=["txt", "pdf", "docx"], accept_multiple_files=True)

# Initialize file_list variable to store names of processed files
file_list = {}


# Add a button to trigger the file upload
if st.button("Upload Files"):
    if uploaded_files:
        # Prepare files to send to the backend
        files_to_send = [
            ("files", (uploaded_file.name, uploaded_file, uploaded_file.type)) for uploaded_file in uploaded_files
        ]
        
        # Send the documents to the backend when the button is clicked
        with st.spinner("Sending the documents to backend..."):
            response = requests.post(backend_url, files=files_to_send)
        
        # Handle the response from the backend
        if response.status_code == 200:
            st.success("Documents Uploaded successfully!")
            file_list = response.json()  # Store the file names returned by the backend
            
        #     # Display the processed file names
        #     if 'files' in file_list:  # Ensure the expected key exists
        #         st.write("Processed Files:")
        #         for file_name in file_list['files']:
        #             st.write(file_name)
        #     else:
        #         st.warning("No files returned from the backend.")
        # else:
        #     st.error(f"Failed to process documents. Status code: {response.status_code}")
    else:
        st.warning("Please upload at least one document before submitting.")









if st.button('Process the Docs for Ingestion into Vector DB'):
    # Get file names from the backend
    with st.spinner("Retrieving files for ingestion..."):
        response = requests.get(files_uploaded_url)
    
    if response.status_code == 200:
        file_list = response.json()

        if 'files' in file_list and file_list['files']:
            st.write("Files ready for ingestion into Vector DB:")
            files_to_ingest = list(file_list['files'])
            st.write(files_to_ingest)

            # Proceed to ingest the files into the Vector DB
            # Correctly format the request for ingestion
            ingestion_response = requests.post(ingestion_url, json=files_to_ingest) # Use 'file_names'
            
            if ingestion_response.status_code == 200:
                st.success("Files successfully ingested into Vector DB")
            else:
                st.error(f"Error in ingestion: {ingestion_response.text}")
        else:
            st.warning("No files available for ingestion.")
    else:
        st.error(f"Error fetching files: {response.text}")









# retrival and generator 


st.title("RAG PDF Q/A")
RAG_URL = 'http://localhost:8000/rag/'

query = st.text_input("Enter your query:")

if st.button("Submit"):
    if query.strip() == "":
        st.error("Please enter a valid Query.")

    else :
        
        response = requests.post(RAG_URL  , json =  {'query' : query})

        
        
        if response.status_code == 200 :
            data = response.json()
            st.success(f"Response: {data['response']}")

            st.success(f"context' : {data['metadata']}")
        else : st.error("Error occured while fetching the response.")


