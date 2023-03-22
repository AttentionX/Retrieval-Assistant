import os
import openai
from dotenv import load_dotenv

load_dotenv()

# Define the OpenAI API parametersx
# openai.api_key = '<YOUR_OPENAI_API_KEY>'
openai.api_key = os.environ.get('OPENAI_API_KEY')

def embedding(text):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input = [text], model="text-embedding-ada-002")['data'][0]['embedding']

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
    
def chatGPT(chat_history):
    engine = "gpt-3.5-turbo"
    system = "You are a helpful assistant. You can answer questions soley based on the information given below. If the question can't be answered with the information given by the user, tell the user that you were unable to find the answer from the given information and ask the user if you should answer the question on you own, without referring to the given information."
    messages = [
        {"role": "system", "content": system},
    ]
    
    messages = messages + chat_history
    
    response = openai.ChatCompletion.create(
        model = engine,
        messages = messages,
    )
    answer = response.choices[0].message.content
    return answer

class customChatGPT:
    def __init__(self, engine, system):
        self.engine = engine
        self.system = system
        self.messages = [{"role": "system", "content": self.system}]

    def chat(self, message):
        # print(self.messages)
        self.messages.append({"role": "user", "content": message})
        
        # print(self.messages)

        response = openai.ChatCompletion.create(
            model = self.engine,
            messages = self.messages,
        )
        answer = response.choices[0].message.content
        self.messages.append({"role": "assistant", "content": answer})
        return answer

class customGPT:
    def __init__(self, engine, prompt):
        self.engine = engine
        self.prompt = prompt

    def chat(self, message):
        response = openai.Completion.create(
            engine=self.engine, 
            prompt=f'{self.prompt}\n{message}',
            temperature=0.1, 
            max_tokens=1000
        )
        answer = response.choices[0]['text']
        return answer    
