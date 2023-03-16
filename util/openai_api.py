import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Define the OpenAI API parametersx
# openai.api_key = '<YOUR_OPENAI_API_KEY>'
openai.api_key = os.environ.get('OPENAI_API_KEY')

def gpt3(fileContent, question):
    # Send the OpenAI API request
    engine = "text-davinci-003"
    max_tokens = 1000
    temperature = 0.1
    response = openai.Completion.create(
        engine=engine, 
        prompt=f'{fileContent}\nQuestion: {question}\nAnswer:',
        temperature=temperature, 
        max_tokens=max_tokens
    )

    # Print the OpenAI API response
    answer = response.choices[0]['text']
    print('OpenAI API response:', answer)
    return answer
    
def chatGPT(fileContent, chat_history):
    engine = "gpt-3.5-turbo"
    system = "You are a helpful assistant. You can answer questions soley based on the information given below. However, if the question can't be answered with the given information, you can answer it without referring to the given information while telling the user that you were unable to retrieve and information from the given information and ask the user for more information."
    messages = [
        {"role": "system", "content": system},
        {"role": "assistant", "content": fileContent},
        # {"role": "user", "content": question}
    ]
    
    messages = messages + chat_history
    
    response = openai.ChatCompletion.create(
        model = engine,
        messages = messages,
    )
    answer = response.choices[0].message.content
    return answer