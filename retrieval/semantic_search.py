from util import mongo_db
import numpy as np
from retrieval.save_document import get_embedding

'''
[Embeddings-based Retriever]
input: question(s), collection_name
process: Retrieve document chunks based on embeddings.
'''

def cos_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a)*np.linalg.norm(b))

def retrieve(questions, collection_name, k=None):
    # Connect to db
    edb = mongo_db.init('embeddings')
    collection = edb[collection_name]
    data = collection.find({})
    
    # Load chunks and thier embeddings from db
    chunks = []
    embeddings = []
    
    for record in data:
        chunks.append(record['chunk'])
        embeddings.append(np.array(record['embedding']))
    
    # Get question embeddings
    question_embeddings = [np.array(get_embedding(question)) for question in questions]
    embeddings = np.array(embeddings).T
    
    # Get similarity between the question and chunks
    embedding_sims = [list(cos_similarity(question_embedding, embeddings)) for question_embedding in question_embeddings]
    chunk_sims = [dict(zip(chunks, list(embedding_sim))) for embedding_sim in embedding_sims]
    chunk_sims = [sorted(chunk_sim.items(),  key = lambda item : item[1], reverse=True) for chunk_sim in chunk_sims]
    
    
    embedding_count = 0
    question_count = len(questions)
    
    result = []
    enable_token_count = 2000
    
    while(True):
        # defines 'for Nth question'
        question_index = embedding_count % question_count
        # defines 'for Nth similar embedding'
        embedding_index = int(embedding_count / question_count)
        
        chunk, _ = chunk_sims[question_index][embedding_index]
        
        # Check for token capacity
        token_count = len(chunk.split(' '))
        enable_token_count -= token_count
        
        if(enable_token_count<0): 
            break
        else:
            # Add chunk to result
            result.append(chunk)
            embedding_count += 1
            
    return result

