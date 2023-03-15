from pymongo import MongoClient

def init():
    # Define the MongoDB database URL and database name
    dbHost = 'localhost'
    dbPort = 27017
    dbName = 'mydb'

    # Connect to the MongoDB database
    client = MongoClient(host=dbHost, port=dbPort)
    db = client[dbName]
    return db