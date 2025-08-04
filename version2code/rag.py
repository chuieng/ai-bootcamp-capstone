import os
import tiktoken
from unittest import loader
from dotenv import load_dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_openai import OpenAIEmbeddings

# load_dotenv()
# OPENAI_KEY = os.getenv('OPENAI_API_KEY')

def count_tokens(text):
    encoding = tiktoken.encoding_for_model('gpt-4o-mini')
    return len(encoding.encode(text))

def load_and_split_pdf(chunk_size=300, chunk_overlap=30): 
    print("loading and splitting pdf...")
    docs_dir = "data/pdf"
    list_of_documents_loaded = []

    # load documents from the data directory
    for filename in os.listdir(docs_dir):
        try:
            path = os.path.join(docs_dir, filename)
            # Load document 
            loader = PyPDFLoader(path)
            print(f"Loading {filename}...")
            list_of_documents_loaded.extend(loader.load())

        except Exception as e:
            print(f"Error loading {filename}: {e}")
            continue

    print("Total documents loaded:", len(list_of_documents_loaded))

    # Split document into smaller overlapping chunks        
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=count_tokens
    )

    splitted_documents = text_splitter.split_documents(list_of_documents_loaded)


    # embedding model that we will use for the session
    embeddings_model = OpenAIEmbeddings(model='text-embedding-3-small')


    # Create the vector database
    vectordb = Chroma.from_documents(
        documents=splitted_documents,
        embedding=embeddings_model,
        collection_name="splitter_threshold", # one database can have multiple collections
        persist_directory="./vector_db"
    )
    print("vectordb collection count=", vectordb._collection.count())