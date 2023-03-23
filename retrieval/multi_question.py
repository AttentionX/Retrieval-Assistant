from util import mongo_db, openai_api
import json

'''
[Question Decomposer]
input: question
process: Decompose the question into subquestions and save into db.
'''

question_decomposition_prompt = '''
    Decompose this question into subquestions that are shorter, and required when answering the original question.
    output form: ["", "", ..., ""]

    Q. What is difference between GPT-3 and BERT?
    ["What is GPT-3?", "What is BERT?", "What are the differences between GPT-3 and BERT?"]

    Q. What is the difference between self attention and multi head attention? How can I use it in transformer?
    ["What is self attention?", "What is multi head attention?", "What are the differences between self attention and multi head attention?", "How can I use self attention and multi head attention in transformer?"]

    Q. I don't understand what is data structure, and how is it used. Tell me more about data structure, regarding to heap sort.
    ["What is data structure?", "How is data structure used?", "What is heap sort?", "How does heap sort work in relation to data structure?"]
    
    Q. 
'''

def decompose_question(question):
    # connect to db
    qdb = mongo_db.init('question')
    collection = qdb['subquestion']
    result = collection.find({'content': question})
    result = list(result)
    
    if(len(result)>0):
        # if subquestions exist, load and return
        print('subquestions loaded from db')
        result = [dic['subquestions'] for dic in result]
        return result
    
    # get subquestions using openai gpt3 api
    prompt = question_decomposition_prompt + question
    response = openai_api.gpt3(prompt)
    
    subquestion_string = response.strip()
    subquestions = json.loads(subquestion_string)
    
    collection.insert_one({'content': question, 'subquestions': subquestion_string})
    return subquestions