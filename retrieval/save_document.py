from util import mongo_db, openai_api
from nltk import tokenize
import numpy as np

# Connect to MongoDB
cdb = mongo_db.init('chunks')
edb = mongo_db.init('embeddings')
qdb = mongo_db.init('question')

'''
[Chunker & Embedder]
input: document, chunk_type, collection_name
process: Chunk the document and save the embeddings into db.
'''

def get_embedding(question):
    embedding = openai_api.embeddings(question)[0]
    return embedding

def create_collection(text, chunk_type=None, title=None):
    if(chunk_type==None): return
    if(title==None):
        title = text[:10]
        
    collection_name = title + '_' + chunk_type
    return collection_name

def get_chunks(text, chunk_type=None):
    if(chunk_type == 'sentence'):
        chunks = list(tokenize.sent_tokenize(text))
        return chunks
    
    elif(chunk_type == 'paragraph'):
        chunks = text.split('\n\n')
        return chunks
    
    else: return None
    
def save_chunks(collection_name, chunks):
    collection = cdb[collection_name]
    for chunk in chunks:
        collection.insert_one({'content': chunk})

def save_embeddings(collection_name, chunks):
    collection = edb[collection_name]
    embeddings = openai_api.embeddings(chunks)
    for chunk, embedding in zip(chunks, embeddings):
        collection.insert_one({'chunk': chunk, 'embedding': embedding})
        
def save_pages_embeddings(collection_name, chunks):
    collection = edb[collection_name]
    embeddings = openai_api.embeddings(chunks)
    page = 1
    for chunk, embedding in zip(chunks, embeddings):
        collection.insert_one({'chunk': chunk, 'embedding': embedding, 'page': page})
        page += 1
        