import numpy as np
import re
import PyPDF2

def max_length(string, max_len):
    if len(string) > max_len:
        return string[:max_len]
    
def process_page(page):
    final_sections = []
    sections = page.split('.\n')
    sections = [re.sub('\s+', ' ', section).strip() for section in sections]

    # print(len(sections), sections[:5])
    # exit()

    skip = []
    i = 0
    j = 0
    for section in sections:
        if i in skip:
            i += 1
            continue
        
        while j < len(sections) - 1 and len(section) < 300:
            j += 1
            section += '. ' + sections[j]
            skip.append(j)
        final_sections.append(section)
        i += 1
        if i > j:
            j = i
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
    # print('keyword: ', keyword)
    count_array = np.array(count_array)
    # print(count_array[:3])
    
    count_array = np.char.count(count_array, keyword)

    # print(count_array[:3])
    # exit()

    # Reshape the count array to a 1D array
    count_1d = count_array.flatten()
    # count_1d = count_array.reshape(-1)

    # print((count_1d.shape))
    
    count_1d = count_1d.astype(float)
    # count_1d = np.array(count_1d).astype(float)

    if np.sum(func(count_1d)) == 0:
        return count_array
    
    # Apply the softmax function to the 1D array
    softmax_1d = func(count_1d) / np.sum(func(count_1d))
    
    # Reshape the softmax output back to the original shape
    softmax_tensor = softmax_1d.reshape(count_array.shape)
    
    # softmax_tensor.tolist()

    return softmax_tensor

def find_highest_positions(arr, k):
    arr = np.array(arr)

    print('process.py, find_highest_positions, first 3 scores:', arr[:3])

    # Flatten the array to 1D and get the indices of the top k values
    flat_indices = np.argsort(arr.flatten())[-k:]

    # Convert the flat indices back to row and column indices
    row_indices, col_indices = np.unravel_index(flat_indices, arr.shape)

    # Print the result
    return list(zip(row_indices, col_indices)) 

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