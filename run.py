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

fileContent = process.max_length(fileContent, 7000)

while True:
    question = input('Ask a question about the file: ')
    
    # Save the question to the database
    # collection = db['questions']
    # collection.insert_one({'question': question})
    chat_history.append({"role": "user", "content": question})
    # print('Question saved to database')
    
    answer = openai_api.chatGPT(fileContent, chat_history)
    print('Answer:', answer)
    
    # Save the answer to the database
    # collection = db['answers']
    # collection.insert_one({'question': question, 'answer': answer})
    chat_history.append({"role": "assistant", "content": answer})
    # print('Answer saved to database')