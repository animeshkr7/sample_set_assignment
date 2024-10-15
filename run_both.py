import subprocess
import threading
import time

# Function to run the FastAPI backend
def run_fastapi():
    subprocess.run(["uvicorn", "backend:app", "--reload"])

# Function to run the Streamlit frontend
def run_streamlit():
    subprocess.run(["streamlit", "run", "app.py"])

# Create threads for both services
fastapi_thread = threading.Thread(target=run_fastapi)
streamlit_thread = threading.Thread(target=run_streamlit)

# Start both threads
fastapi_thread.start()

time.sleep(30)
streamlit_thread.start()

# Join both threads to ensure they continue running
fastapi_thread.join()

streamlit_thread.join()
