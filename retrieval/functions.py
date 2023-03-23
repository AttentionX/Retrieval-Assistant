from retrieval.save_document import create_collection, get_chunks, save_chunks, save_embeddings
import retrieval.keyword_search as keyword_search
from retrieval.multi_question import decompose_question
import retrieval.semantic_search as semantic_search
import time

def save_to_db(document, chunk_type='paragraph', title=None): 
    description = '''
        [Chunker & Embedder]
        input: document, chunk_type, title
        process: Chunk the document and save the embeddings into db.
        output: collection_name
    '''
    print(description)
    print(f'Input Title: {title}')
    
    start = time.time()
    
    collection_name = create_collection(document, chunk_type, title)
    if(collection_name==None): 
        return None
    chunks = get_chunks(document, chunk_type)
    
    save_chunks(collection_name, chunks)
    save_embeddings(collection_name, chunks)
    
    end = time.time()
    
    runtime = end - start
    print(f'Output Collection Name: {collection_name}\nRuntime: {runtime}')
    return collection_name
    

def extract_keyword(question): 
    description = '''
        [Question Keyword Extractor]
        input: question
        process: Extract keywords from the question and save into db.
        output: keywords
    '''
    print(description)
    print(f'Input Question: {question}')
    
    start = time.time()
    keywords = keyword_search.get_keywords(question)
    end = time.time()
    
    runtime = end - start
    print(f'Output Keywords: {keywords}\nRuntime: {runtime}')
    return keywords


def keyword_based_retrieval(keywords, collection_name):
    description = '''
        [Keyword-based Retriever]
        input: keywords, collection_name
        process: Retrieve document chunks based on keywords.
        output: chunks
    '''
    print(description)
    
    start = time.time()
    chunks = keyword_search.retrieve(keywords, collection_name)
    end = time.time()
    
    k = len(chunks)
    runtime = end - start
    print(f'Output {k} Chunks: {chunks}\nRuntime: {runtime}')
    return chunks
    
    
def decompose_question(question): 
    description = '''
        [Question Decomposer]
        input: question
        process: Decompose the question into subquestions and save into db.
        output: subquestions
    '''
    print(description)
    print(f'Input Question: {question}')
    
    start = time.time()
    subquestions = decompose_question(question)
    end = time.time()
    
    runtime = end - start
    print(f'Output Subquestions: {subquestions}\nRuntime: {runtime}')
    return subquestions


def embedding_based_retrieval(questions, collection_name):
    description = '''
        [Embeddings-based Retriever]
        input: question(s), collection_name
        process: Retrieve document chunks based on embeddings.
        output: chunks
    '''
    print(description)
    
    start = time.time()
    chunks = semantic_search.retrieve(questions, collection_name)
    end = time.time()
    
    k = len(chunks)
    runtime = end - start
    print(f'Output {k} Chunks: {chunks}\nRuntime: {runtime}')
    return chunks

# Retrievers

def k1(question, collection_name):
    print('------------------------K1------------------------')
    keywords = extract_keyword(question)
    chunks = keyword_based_retrieval(keywords, collection_name)
    return chunks
    
def s1(question, collection_name):
    print('------------------------S1------------------------')
    chunks = embedding_based_retrieval([question], collection_name)
    return chunks

def s2(question, collection_name):
    print('------------------------S2------------------------')
    subquestions = decompose_question(question)
    chunks = embedding_based_retrieval(subquestions, collection_name)
    return chunks