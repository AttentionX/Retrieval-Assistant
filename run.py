import sys

from util import mongo_db, openai_api, pdf_to_txt, process

file_path = './samples/papers/transformer.txt'

if len(sys.argv) == 2:
    file_path = sys.argv[1]

if(file_path.endswith('.pdf')):
    print('PDF file detected')
    pages = pdf_to_txt.convert(file_path)
    fileContent = '\n\n'.join(pages)
else:
    # Read the file content
    with open(file_path, 'r', encoding='utf-8') as file:
        fileContent = file.read()

db = mongo_db.init()

chat_history = []

fileContent = process.max_length(fileContent, 15000)

chat_instruction = "You are a helpful assistant. You can answer questions soley based on the information given below. If the question can't be answered with the information given by the user, tell the user that you were unable to find the answer from the given information and ask the user if you should answer the question without referring to the given information."
examples = '''
For example, if the user asks a question that can't be answered with the given information, respond as follows:
User: What is the GPT-10 architecture?
Assistant: The infomation on the GPT-10 architecture is not provided in the information you have provided. Should I answer the question without referring to the given information?
'''
prompt = f'Given Information:\n----------\n{fileContent}\n----------'

chat_history.append({"role": "assistant", "content": prompt})

while True:
    question = input('Ask a question about the file: ')
    
    # Save the question to the database
    # collection = db['questions']
    # collection.insert_one({'question': question})
    chat_history.append({"role": "user", "content": question})
    # print('Question saved to database')
    
    answer = openai_api.chatGPT(chat_history)
    print('Answer:', answer)
    
    # Save the answer to the database
    # collection = db['answers']
    # collection.insert_one({'question': question, 'answer': answer})
    chat_history.append({"role": "assistant", "content": answer})
    # print('Answer saved to database')