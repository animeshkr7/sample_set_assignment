# used this module for retriving relent context 
# and generating response from Mistral AI using HuggingFace
# retiver and generator both inside same componet (ie.e  rag chain)


"""
METHODS 
1) create_prompts(query , context)
2) retriver_and_LLM_Generation

"""


from langchain.prompts import ChatPromptTemplate
from langchain import HuggingFaceHub
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from dotenv import load_dotenv
import os

load_dotenv()





def create_prompts():

    template = """

    You are an assistant for question - answering task.
    Use the following piece of retrived context to answer the question.
    If you don't know , just respond "Out of My context"

    Use 5 sentence at maximum and keep the answer concie.

    ONLY RESOPNSE SHOULD BE ANSWER NOTHING ELSE

    Question : {query}

    Context_rag : {context}

    Answer_rag : 

    """

    prompt = ChatPromptTemplate.from_template(template)

    return prompt




def retriever_and_LLM_Generation(vector_db, prompt, query):
    huggingface_api_token = os.getenv("HUGGINGFACE_TOKEN")

    model = HuggingFaceHub(
        huggingfacehub_api_token=huggingface_api_token,
        repo_id='mistralai/Mistral-7B-Instruct-v0.1',
        model_kwargs={'temperature': 1, "max_length": 180}
    )

    output_parser = StrOutputParser()
    retriever = vector_db.as_retriever()

    rag_chain = (
        {'context': retriever, 'query': RunnablePassthrough()}
        | prompt
        | model
        | output_parser
    )

    output = rag_chain.invoke(query)

    # Optional: Extract the context from the output if needed
    # Assuming that the output includes both the context and the answer
    index = output.find('Answer_rag')
    answer = output[index:]

    # If you want to return the context as well, you may need to adjust this based on your implementation
    context_index = output.find('Context_rag')
    context = output[context_index:index] if context_index != -1 else "No context retrieved."
    context = context

    return answer , context