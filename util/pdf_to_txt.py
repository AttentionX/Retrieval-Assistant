import PyPDF2
 
file_path = '../samples/papers/transformer.pdf'

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
        pages.append(text)
    
    # Close the file object
    pdf_file.close()
    
    return pages
 
def convert(file_path):
    text = '\n'.join(pages(file_path))
    return text
