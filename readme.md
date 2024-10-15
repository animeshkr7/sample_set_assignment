



To use it :

- Clone the Repository

- Upload the weaviate cluster api  , weaviate KEY , huggingFace Token

- Create environment :
CMD:

`` python -m venv myenv

- Activate Environment
CMD:

`` myenv\Scripts\activate


- Install Requirements.txt

``pip install requirements.txt

If want to run frontend and backend separately , then open 2 terminals with environment activated then :



#### Running the FastAPI backend 
`` uvicorn backend:app --reload 


### Running the Front End

`` streamlit run app.py


ELSE : CMD : ( may occur issue of update the backend code while experimenting)

`` python run_both.py






