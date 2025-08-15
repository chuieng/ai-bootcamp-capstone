import os
import streamlit as st
from dotenv import load_dotenv
from smolagents import tool, Tool, CodeAgent, OpenAIServerModel


@tool
def get_answer(question: str) -> dict:
   """
   Return the answer to the question based on the HDB document collection from session state.

   Args:
      question: the question to be answered

   Returns:
      dict: the answer to the question

   Example:
      result = get_answer('What is Option to Purchase?')
   """
   # Get the collection from Streamlit session state
   if 'hdb_documents_collection' not in st.session_state:
       return {'question': question, 'error': 'ChromaDB hdb doc collection not found in session state'}
   
   hdb_doc_collection = st.session_state.hdb_documents_collection
   print(f"Using collection: {hdb_doc_collection.name} with {hdb_doc_collection.count()} documents")
   
   results = hdb_doc_collection.query(
      query_texts=[question],
      n_results=5,
   )
   return {'question': question, 'answer': results['documents'][0]}


def create_agent():
    # Load environment variables
   #  load_dotenv()
    OPENAI_KEY = st.secrets.get("OPENAI_API_KEY")
    
    if not OPENAI_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    
    # Load an agent model
    model = "gpt-4o-mini"  # Fixed model name
    
    # Create the model for the agent to use
    agent_model = OpenAIServerModel(model_id=model, api_key=OPENAI_KEY)
    
    # Create an agent with our own tools
    tools = [get_answer]
    
    agent = CodeAgent(tools, model=agent_model, add_base_tools=False, max_steps=5)
    print(f"Agent created with model: {model}")
    return agent


def query_agent(agent, question):
   prompt = f"""
   You are a helpful assistant that only answers questions based on the following official HDB documents related to resale flats in Singapore.
   
   QUESTION:
   "{question}"

   GUIDELINES:
   - Use only the provided documents to answer.
   - Present your answer in a clear, concise paragraph format.
   - If the documents do not contain relevant information, respond with: **"Please contact HDB for assistance."**
   - Do NOT make up information. Do not use the Internet.
   - Be concise and accurate. Avoid repeating the question.
   - Answer in a professional and helpful manner.
   Answer:
   """
   return agent.run(prompt)