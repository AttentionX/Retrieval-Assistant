import openai

# Define the OpenAI API parameters
openai.api_key = '<YOUR_OPENAI_API_KEY>'

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
    system = "You are a helpful assistant."
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