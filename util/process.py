import numpy as np
import re
import PyPDF2

def max_length(string, max_len):
    if len(string) > max_len:
        return string[:max_len]
    
def process_page(page):
    final_sections = []
    sections = page.split('\n')
    for section in sections:
        # Remove redundant spaces
        section = re.sub('\s+', ' ', section)
        # Remove space at the beginning of the string
        section = section.strip()
        if len(section) > 50:
            final_sections.append(section)
    return final_sections

def process_pages(pages):
    procedded_pages = []
    for page in pages:
        procedded_pages.append(process_page(page))
    return procedded_pages

def getFileInfo(file_path):
    if(file_path.endswith('.pdf')):
        print('PDF file detected')
        pages = convert(file_path)
        # 2D Array
        fileContent = process_pages(pages)
        return 'pdf', fileContent
    else:
        # Read the file content
        with open(file_path, 'r', encoding='utf-8') as file:
            fileContent = file.read()
            # 1D Array
            fileContent = process_page(fileContent)
        return 'txt', fileContent
    
def operate_2d_tensor(count_array, keyword, func):
    print('keyword: ', keyword)
    count_array = np.array(count_array)

    
    count_array = np.char.count(count_array, keyword)

    # Reshape the count array to a 1D array
    count_1d = count_array.flatten()
    # count_1d = count_array.reshape(-1)

    # print((count_1d.shape))
    
    count_1d = count_1d.astype(float)
    # count_1d = np.array(count_1d).astype(float)
    
    # Apply the softmax function to the 1D array
    softmax_1d = func(count_1d) / np.sum(func(count_1d))
    
    # Reshape the softmax output back to the original shape
    softmax_tensor = softmax_1d.reshape(count_array.shape)
    
    return softmax_tensor.tolist()

def find_highest_positions(arr, k):
    arr = np.array(arr)

    # Flatten the 2D array into a 1D array
    arr_flat = arr.flatten()
    
    # Find the indices of the k highest values in the flattened array
    indices_flat = np.argpartition(arr_flat, -k)[-k:]
    
    # Convert the flattened indices back to row and column indices in the 2D array
    indices_rc = np.unravel_index(indices_flat, arr.shape)
    
    # Reverse the order of the indices so that the highest values come first
    indices_rc = list(reversed(indices_rc))
    
    # Return the list of (row, column) tuples
    return list(zip(*indices_rc))

def convert(file_path):
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
        text = pdf_reader.pages[page].extract_text().lower().strip()
        pages.append(text)
        # print(text)
    
    # Close the file object
    pdf_file.close()
    
    return pages