from util import mongo_db, openai_api

# Read the file content
with open('file.txt', 'r', encoding='utf-8') as file:
    fileContent = file.read()

while True:
    question = input('Ask a question about the file: ')
    
    # Save the question to the database
    collection = mongo_db.db['questions']
    collection.insert_one({'question': question})
    print('Question saved to database')
    
    answer = openai_api.chatGPT(fileContent, question)
    
    # Save the answer to the database
    collection = mongo_db.db['answers']
    collection.insert_one({'question': question, 'answer': answer})
    print('Answer saved to database')