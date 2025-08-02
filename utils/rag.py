# Imports
import json, random
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter, RecursiveJsonSplitter

def print_chunk_info(chunks):
    """Print information about document chunks including total count and details of a random chunk."""
    print(f'No of chunks: {len(chunks)}')
    idx = random.randrange(0, len(chunks))
    print(f'Chunk index: {idx}')
    print('Chunk details')
    for k, v in enumerate(chunks[idx]):
        print(f'\t{k} = {v}')

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

# For backwards compatibility and testing
if __name__ == "__main__":
    chunks = process_all_hdb_documents()