from pymongo import MongoClient

my_client = MongoClient("mongodb://localhost:27017/")
print(my_client.list_database_names())

mydb = my_client['test']
mycol = mydb['blog']

# #한개만 입력
# x = mycol.insert_one({"name": "insung", "address": "guㅇro, seoul"})
# #print(x.inserted_id)
#
# #한개만 출력
# x = mycol.find_one()
# print(x)

#여러개 입력
# my_dict = [{"name": "putty", "address": "network"},
#            {"name": "dong", "address": "korea"},
#            {"name": "bok", "address": "japan"}]

# y = mycol.insert_many(my_dict)
#print(x.inserted_ids)

#여러개 출력
# list = mycol.find()
#
# for x in list:
#     print(x)

# #오름차순으로 정렬 출력
# my_doc = mycol.find().sort("name")
# for x in my_doc:
#     print(x)
#내림차순으로 정렬 출력
# my_doc = mycol.find().sort("name", -1)
# for x in my_doc:
#     print(x)

#원하는 쿼리를 통해 결과 필터링하여 출력
# my_query = {"address": "korea"}
# my_doc = mycol.find(my_query)
# for x in my_doc:
#     print(x)

#비교연산 쿼리를 통해 필터링하여 출력
# my_query = {"name": {"$gt": "e"}}
# my_doc = mycol.find(my_query)
# for x in my_doc:
#     print(x)

#정규식 쿼리를 통해 필터링하여 출력(대소문자 따진다)
# my_query = {"name": {"$regex": "^b"}}
# my_doc = mycol.find(my_query)
# for x in my_doc:
#     print(x)


