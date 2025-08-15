__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import streamlit as st
import chromadb
import os

from utils.check_pw import check_password
from chromadb.utils import embedding_functions
from utils.agent_tool import create_agent, query_agent
from utils.helper import sanitize_response


# Initialize ChromaDB collection in session state
if 'hdb_documents_collection' not in st.session_state:
    print("loading hdb_documents_collection into session state")
    # Connect to persistent ChromaDB client
    client = chromadb.PersistentClient(path="./chroma_db")
    
    # Create the same embedding function used during collection creation
    embed_model_name = "BAAI/bge-small-en-v1.5"
    embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embed_model_name)
    
    # Get the existing collection and store in session state
    st.session_state.hdb_documents_collection = client.get_collection(name="hdb_documents", embedding_function=embed_func)
    print(f"loaded hdb_documents_collection into session state - {st.session_state.hdb_documents_collection.count()} chunks")

st.set_page_config(
    layout="wide",
    page_title="HDB Resale Process Assistant"
)

# Do not continue if check_password is not True.  
if not check_password():  
    st.stop()

st.title("💬 HDB Resale Process Assistant")

# Welcome message
st.write("""Hello! I'm your HDB Resale Process Assistant.

I have access to comprehensive information about:
- 🏠 Resale Process & Procedures
- 💰 Financial Planning
- 📋 Policies & Requirements
- 🎯 Planning Considerations

Example questions: "What documents do I need for HDB resale?" or "How does the Option to Purchase work?"
""")

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("What would you like to ask?"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate a response using the agent with RAG
    with st.chat_message("assistant"):
        with st.spinner("Searching HDB documents..."):
            try:
                # Create agent if not in session state
                if 'agent' not in st.session_state:
                    st.session_state.agent = create_agent()
                
                # Query the agent with RAG capabilities
                response = query_agent(st.session_state.agent, prompt)
                sanitized_response = sanitize_response(response)
                st.write(sanitized_response)
                
            except Exception as e:
                response = f"Sorry, I encountered an error: {str(e)}"
                st.write(response)
    
    st.session_state.messages.append({"role": "assistant", "content": sanitized_response})