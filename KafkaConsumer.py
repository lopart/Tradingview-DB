import json
from kafka import KafkaConsumer
from pymongo import MongoClient

client = MongoClient("********") ## "mongodb+srv://<username>:<password>@<cluster-name>.mongodb.net/myFirstDatabase" or 
                                 ## in MongoDB Atlas account see 'Database' --> 'Connect' --> 'Connect your application' --> 'Add your connection string into your application code'
db = client["mongoDB_name"]
col = db["collection_name"] 


consumer = KafkaConsumer('topic_name')

for msg in consumer:
    msg_json = json.loads(msg.value)
    print(col.insert_one(msg_json).inserted_id)
