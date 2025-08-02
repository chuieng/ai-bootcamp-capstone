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

def process_hdb_documents(print_info=True):
    """
    Process HDB documents and return chunks.
    
    Args:
        print_info (bool): Whether to print chunk information (default: True)
    
    Returns:
        list: List of document chunks from HDB Buying Procedure PDF
    """
    print("Processing HDB documents...")
    file_path = "data/pdf/HDB _ Buying Procedure for Resale Flats.pdf"
    chunks = load_and_split_pdf(file_path)
    
    if print_info:
        print_chunk_info(chunks)
    
    return chunks

def load_multiple_pdfs(file_paths, chunk_size=300, chunk_overlap=30, extract_images=True):
    """
    Load multiple PDF files and split them into chunks.
    
    Args:
        file_paths (list): List of paths to PDF files
        chunk_size (int): Size of each text chunk (default: 300)
        chunk_overlap (int): Overlap between chunks (default: 30)
        extract_images (bool): Whether to extract images from PDF (default: True)
    
    Returns:
        list: Combined list of document chunks from all PDFs
    """
    print(f"Loading {len(file_paths)} PDF files...")
    all_chunks = []
    
    for file_path in file_paths:
        try:
            print(f"Processing: {file_path}")
            chunks = load_and_split_pdf(file_path, chunk_size, chunk_overlap, extract_images)
            all_chunks.extend(chunks)
            print(f"✅ Added {len(chunks)} chunks from {file_path}")
        except Exception as e:
            print(f"❌ Error processing {file_path}: {str(e)}")
    
    print(f"Total chunks loaded: {len(all_chunks)}")
    return all_chunks

def load_pdfs_from_directory(directory_path, chunk_size=300, chunk_overlap=30, extract_images=True):
    """
    Load all PDF files from a directory and split them into chunks.
    
    Args:
        directory_path (str): Path to directory containing PDF files
        chunk_size (int): Size of each text chunk (default: 300)
        chunk_overlap (int): Overlap between chunks (default: 30)
        extract_images (bool): Whether to extract images from PDF (default: True)
    
    Returns:
        list: Combined list of document chunks from all PDFs in directory
    """
    import os
    
    # Get all PDF files in the directory
    pdf_files = []
    if os.path.exists(directory_path):
        for file in os.listdir(directory_path):
            if file.lower().endswith('.pdf'):
                pdf_files.append(os.path.join(directory_path, file))
    else:
        print(f"Directory not found: {directory_path}")
        return []
    
    print(f"Found {len(pdf_files)} PDF files in {directory_path}")
    
    if not pdf_files:
        print("No PDF files found in directory")
        return []
    
    return load_multiple_pdfs(pdf_files, chunk_size, chunk_overlap, extract_images)

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
    chunks = process_hdb_documents()