from util import mongo_db, openai_api
import json

'''
[Question Keyword Extractor]
input: question
process: Extract keywords from the question and save into db.
'''
keyword_extraction_prompt = '''
        Extract keywords from this question in this output form:
        output form: ["", "", ..., ""]

        Example
        Q. What is difference between GPT-3 and BERT?
        ["difference", 'GPT-3', 'BERT']

        Q. What is the difference between self attention and multi head attention? How can I use it in transformer?
        ["difference", "self attention", "multi head attention", "use", "transformer"]

        Q. 
    '''
    
def get_keywords(text):
    # connect to db
    qdb = mongo_db.init(dbName='question')
    collection = qdb['keyword']
    results = collection.find({'content': text})
    results = list(results)
    
    if(len(results)>0):
        # if keywords exist in db, load and return
        print('keywords loaded from db')
        results = [dic['keywords'] for dic in results]
        keywords = []
        for result in results:
            keywords += json.loads(result.strip())
        return keywords
    
    # get keywords using openai gpt3 api
    prompt = keyword_extraction_prompt + text
    response = openai_api.gpt3(prompt)
    
    keyword_string = response.strip()
    keywords = json.loads(keyword_string)
    
    collection.insert_one({'content': text, 'keywords': keyword_string})
    return keywords

'''
[Keyword-based Retriever]
input: keywords, collection_name
process: Retrieve document chunks based on keywords.
'''

def retrieve(keywords, collection_name):
    # create 'text' index to the collection (for text search)
    cdb = mongo_db.init(dbName='chunks')
    collection = cdb.get_collection(collection_name)
    collection.create_index([('content', 'text')])
    
    # concatenate keywords as string
    keyword_string = ''
    for keyword in keywords:
        keyword_string += keyword+' '
    print('Keywords: ', keyword_string)
    print(collection_name)
    
    # retrieve chunks from db
    chunks = collection.find({'$text': {'$search': keyword_string}})
    
    result = []
    enable_token_count = 600
    for chunk in chunks:
        content = chunk['content']
        
        # check for token capacity
        token_count = len(content.split(' '))
        enable_token_count -= token_count
        if(enable_token_count<0): 
            break
        else:
            # add to result
            result.append(content)
    return result