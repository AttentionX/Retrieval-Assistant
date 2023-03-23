import PyPDF2
from util import mongo_db, openai_api, pdf_to_txt, process
from retrieval.save_document import create_collection, save_pages_embeddings
from retrieval.functions import save_to_db

def pages(file_path):
    # Create file object variable
    # Opening method will be rb
    pdf_file = open(file_path,'rb')
    
    # Create reader variable that will read the pdffileobj
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    
    # This will store the number of pages of this pdf file
    num_pages = len(pdf_reader.pages)
    
    pages = []

    # Print the text of each page in the pdf file
    for page in range(num_pages):
        text = pdf_reader.pages[page].extract_text()
        pages.append(str(text))
    
    # Close the file object
    pdf_file.close()
    
    return pages

def save_pages(file_path):
    pages = pages(file_path)
    collection_name = create_collection(text=pages[0], chunk_type='page', title='hw2')
    save_pages_embeddings(collection_name, pages)
    return collection_name
 
def save_chunks(file_path, chunk_type='paragraph'):
    # Read the file and convert it to a readable format

    if(file_path.endswith('.pdf')):
        print('PDF file detected')
        fileContent = pdf_to_txt.convert(file_path)
    else:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            fileContent = file.read()

    # fileContent = process.max_length(fileContent, 15000)

    # Save chunks and embeddings of the document
    # chunk_types: 'paragraph', 'sentence', 'page', etc.
    chunk_type = 'paragraph'
    collection_name = save_to_db(fileContent, chunk_type, 'hw2')
    return collection_name