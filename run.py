from pymongo import MongoClient
import openai

# Define the MongoDB database URL and database name
dbHost = 'localhost'
dbPort = 27017
dbName = 'mydb'

# Define the OpenAI API parameters
openai.api_key = '<YOUR_OPENAI_API_KEY>'

# Read the file content
with open('file.txt', 'r', encoding='utf-8') as file:
    fileContent = file.read()

# Connect to the MongoDB database
client = MongoClient(host=dbHost, port=dbPort)
db = client[dbName]

while True:
    question = input('Ask a question about the file: ')
    
    # Save the question to the database
    collection = db['questions']
    collection.insert_one({'question': question})
    print('Question saved to database')
    
    # Send the OpenAI API request
    engine = "text-davinci-003"
    max_tokens = 50
    temperature = 0.5
    response = openai.Completion.create(
        engine=engine, 
        prompt=f'{fileContent}\nQuestion: {question}\nAnswer:',
        temperature=temperature, 
        max_tokens=max_tokens
    )

    # Print the OpenAI API response
    answer = response.choices[0]['text']
    print('OpenAI API response:', answer)
    
    # Save the answer to the database
    collection = db['answers']
    collection.insert_one({'question': question, 'answer': answer})
    print('Answer saved to database')