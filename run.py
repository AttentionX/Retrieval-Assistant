from util import mongo_db, openai_api, pdf_to_txt, process
from save import save_chunks
from retrieval.functions import s1, s2, k1, k2

from samples.books.intro_to_computing import text as computing_text
from samples.lectures.vm import text as vm_text
from samples.lectures.cs224n_2023_lecture10_nlg import text as cs224n_text
from samples.papers.language_fewshot import text as language_fewshot_text
from samples.papers.transformer import text as transformer_text

# save file as chunks to db, and get collection name
file_path = 'samples/assignments/HW 2 - OOP with JAVA(4.12).pdf'
collection_name = save_chunks(file_path=file_path, chunk_type='paragraph') # or just write the collection name in your db

# Chat Setup
db = mongo_db.init()

chat_history = []

examples = '''
For example, if the user asks a question that can't be answered with the given information, respond as follows:
User: What is the GPT-10 architecture?
Assistant: The infomation on the GPT-10 architecture is not provided in the information you have provided. Should I answer the question without referring to the given information?
'''

multi_question_handling_example = '''
If the user's query contains multiple questions, respond as follows:
User's Query: What is the GPT-3 architecture and what training data was used to train GPT-3?
Question1: What is the GPT-3 architecture?
Question2: What is the GPT-3 training data?
'''

# prompt = f'Given Information:\n----------\n{fileContent}\n----------'
prompt = 'You are a paper reading assistant. Answer the question based on the given file.'
prompt += examples
prompt += multi_question_handling_example

chat_history.append({"role": "system", "content": prompt})

while True:
    question = input('Ask a question about the file: ')
    # What is Transformer, and what is self-attention, and how is it used in the paper?
    
    # Get chunks using retriever (k1, k2, s1, s2)
    # (Ex) k1(question, collection_name), s2(question, collection_name)
    chunks = s1(question, collection_name)
    
    prompt = 'Given Information:\n----------\n'
    for chunk in chunks:
        prompt += f'{chunk}\n\n'
    prompt += '\n----------'
    
    chat_history.append({"role": "assistant", "content": prompt})
    
    # Save the question to the database
    collection = db['questions']
    collection.insert_one({'question': question})
    chat_history.append({"role": "user", "content": question})
    print('Question saved to database')
    
    answer = openai_api.chatGPT(chat_history)
    print('Answer:', answer)
    
    # Save the answer to the database
    collection = db['answers']
    collection.insert_one({'question': question, 'answer': answer})
    chat_history.append({"role": "assistant", "content": answer})
    print('Answer saved to database')