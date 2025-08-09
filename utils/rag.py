# Imports
import json, random
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, RecursiveJsonSplitter
import chromadb
from uuid import uuid4
from chromadb.utils import embedding_functions

def load_and_split_pdf(file_path, chunk_size=300, chunk_overlap=30, extract_images=True):
    """
    Load a PDF file and split it into chunks.
    
    Args:
        file_path (str): Path to the PDF file
        chunk_size (int): Size of each text chunk (default: 300)
        chunk_overlap (int): Overlap between chunks (default: 30)
        extract_images (bool): Whether to extract images from PDF (default: True)
    
    Returns:
        list: List of document chunks
    """
    print("loading and splitting pdf...")
    # Create a text splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, 
        chunk_overlap=chunk_overlap
    )
    
    # Load PDF
    pdf_loader = PyPDFLoader(file_path=file_path, extract_images=extract_images)
    chunks = pdf_loader.load_and_split(text_splitter)
    
    return chunks

def process_all_hdb_documents(print_info=True, chunk_size=300, chunk_overlap=30):
    """
    Process all HDB documents from the data directory.
    
    Args:
        print_info (bool): Whether to print chunk information (default: True)
        chunk_size (int): Size of each text chunk (default: 300)
        chunk_overlap (int): Overlap between chunks (default: 30)
    
    Returns:
        dict: Dictionary with file names as keys and their chunks as values
    """
    print("Processing all HDB documents...")
    
    # List of all HDB PDF files
    hdb_files = [
        "data/pdf/HDB _ Buying Procedure for Resale Flats.pdf",
        "data/pdf/HDB _ Ethnic Integration Policy (EIP) and Singapore Permanent Resident (SPR) Quota.pdf",
        "data/pdf/HDB _ Managing the Flat Purchase.pdf",
        "data/pdf/HDB _ Mode of Financing.pdf",
        "data/pdf/HDB _ Option to Purchase.pdf",
        "data/pdf/HDB _ Overview.pdf",
        "data/pdf/HDB _ Planning Considerations.pdf",
        "data/pdf/HDB _ Request for Value.pdf"
    ]
    
    document_chunks = {}
    all_chunks = []
    
    for file_path in hdb_files:
        try:
            print(f"Processing: {file_path}")
            chunks = load_and_split_pdf(file_path, chunk_size, chunk_overlap)
            
            # Extract filename for the key
            filename = file_path.split('/')[-1]
            document_chunks[filename] = chunks
            all_chunks.extend(chunks)
            
            print(f"✅ Loaded {len(chunks)} chunks from {filename}")
            
            if print_info and chunks:
                print(f"Sample from {filename}: {chunks[0].page_content[:100]}...")
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {str(e)}")
    
    print(f"\nTotal files processed: {len(document_chunks)}")
    print(f"Total chunks: {len(all_chunks)}")
    
    return document_chunks, all_chunks

def create_pdf_collection(chunks):
    """
    Create a collection from the document chunks.

    Args:
        chunks (list): List of document chunks

    Returns:
        list: List of dictionaries with chunk content and metadata
    """
    # Create embedding model
    embed_model_name = "BAAI/bge-small-en-v1.5"

    embed_func = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=embed_model_name)

    # Check if chunks is accidentally a tuple (common mistake)
    if isinstance(chunks, tuple):
        print("WARNING: chunks is a tuple, extracting the actual chunks list...")
        _, chunks = chunks  # Get the second element (all_chunks)
    
    # Prepare the chunks for inserting into Chroma
    # extract page_content from the chunks into an array
    texts = [ d.page_content for d in chunks ]
    print(f"Prepare the chunks for inserting into Chroma: {len(texts)}")

    # for every text, generate a unique id for the text
    ids = [ str(uuid4())[:8] for _ in range(len(texts)) ]
    print(f"Generated IDs for chunks: {ids}")

    # Create persistent Chroma client and save chunks
    col_name = 'hdb_documents'

    # create the persistent chroma client
    ch_client = chromadb.PersistentClient(path="./chroma_db")
    try:
        ch_client.delete_collection(col_name)
    except:
        pass

    # create the collection using embedding function
    hdb_doc_collection = ch_client.create_collection(name=col_name, embedding_function=embed_func)

    # Print number of documents in collection
    print('before inserting: ', hdb_doc_collection.count())

    # Add text into collection
    hdb_doc_collection.add(documents=texts, ids=ids)

    # Print number of documents in collection
    print('after inserting: ', hdb_doc_collection.count())

    return hdb_doc_collection

# For backwards compatibility and testing
if __name__ == "__main__":
    print("Starting RAG processing...")
    document_chunks, all_chunks = process_all_hdb_documents()
    create_pdf_collection(all_chunks)