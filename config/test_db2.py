from pymongo import MongoClient

my_client = MongoClient("mongodb://localhost:27017/")

mydb = my_client['test']
mycol = mydb['blog']

x = mycol.insert_one({"name": "insung", "address": "guㅇro, seoul"})
print(x.inserted_id)
