from pymongo import MongoClient

def init(dbName='mydb'):
    # Define the MongoDB database URL and database name
    dbHost = 'localhost'
    dbPort = 27017

    # Connect to the MongoDB database
    client = MongoClient(host=dbHost, port=dbPort)
    db = client[dbName]
    return db