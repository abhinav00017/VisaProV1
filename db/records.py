import json
import pymongo
import logging
from pymongo import MongoClient

class Records:
    def __init__(self):
        self.uri = "mongodb+srv://VisaPro:1OXwJt73cMNtp42s@cluster0.ucnfb3p.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = MongoClient(self.uri)
        self.database = self.client["abhinav"]
        self.collection = self.database["VisaPro"]
        logging.info("Connected to the database")
    
    def create_record(self, record):
        try:
            result = self.collection.insert_one(record)
            logging.info(f"Insert acknowledged: {result.acknowledged}")
            return True
        except Exception as e:
            logging.error(e)
            return False

    def retrieve_record(self, email_id):
        try:
            result = self.collection.find_one({'email': email_id})
            return result
        except Exception as e:
            logging.error(e)
            return None

    def update_record(self, record):
        try:
            query_filter = {'email': record['email']}
            update_operation = {'$set': {key: value for key, value in record.items() if key != 'email'}}
            result = self.collection.update_many(query_filter, update_operation)
            return "Updated The Record"
        except Exception as e:
            logging.error(e)
            return None
    
    
# rec = Records()

# print(rec.create_record(
#         {
#             "email": "abhiteftest@gmail.com",
#             "country": "Russia", 
#             "user_name": "Abhinav", 
#             "threads": [
#                 {"id": "thread_7tV9XZvqxPV91EFRnXM2WTlo", "object": "thread", "created_at": 1719124764, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_N1QKAVDeFClesst21HlSTvI6", "object": "thread", "created_at": 1719124979, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_syRcqzs1zswTNc6xeoI1WE5K", "object": "thread", "created_at": 1719125227, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_zAFWXIqEtaRWECwQxrDydJun", "object": "thread", "created_at": 1719126128, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_spaNRZInvmV5QjfvHAM6NFRG", "object": "thread", "created_at": 1719126133, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_IYAvGpNDjahVKLejU71OOMyO", "object": "thread", "created_at": 1719126831, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_S6aPkjuovmIV8z2enwlUWTdl", "object": "thread", "created_at": 1719126964, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_3EX2cwlBKvkl6KBD6jIx3HlS", "object": "thread", "created_at": 1719127074, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_151AGboKqEk6eDRsmQWDMWr3", "object": "thread", "created_at": 1719127161, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_x6iu5GTiO5RYMbxpxEu4QWoB", "object": "thread", "created_at": 1719127387, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_raxmezQqH0XN8I96H18hNhot", "object": "thread", "created_at": 1719127462, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_rlEUn63EWVUglGGBxbjYzpnP", "object": "thread", "created_at": 1719127831, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_v78Bu9onmiVT56vwp6SG54ao", "object": "thread", "created_at": 1719128269, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_c7LnPGwfzSHFFnXxl0wW7DGZ", "object": "thread", "created_at": 1719128286, "metadata": {"action": "False"}, "tool_resources": {}}
#             ]
#         }
#     )
# )

# print(rec.retrieve_record('abhiteftest@gmail.com'))
# print(rec.update_record(
#         {
#             "email": "abhiteftest@gmail.com",
#             "country": "Russia", 
#             "user_name": "Abhinavv", 
#             "threads": [
#                 {"id": "thread_7tV9XZvqxPV91EFRnXM2WTlo", "object": "thread", "created_at": 1719124764, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_N1QKAVDeFClesst21HlSTvI6", "object": "thread", "created_at": 1719124979, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_syRcqzs1zswTNc6xeoI1WE5K", "object": "thread", "created_at": 1719125227, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_zAFWXIqEtaRWECwQxrDydJun", "object": "thread", "created_at": 1719126128, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_spaNRZInvmV5QjfvHAM6NFRG", "object": "thread", "created_at": 1719126133, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_IYAvGpNDjahVKLejU71OOMyO", "object": "thread", "created_at": 1719126831, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_S6aPkjuovmIV8z2enwlUWTdl", "object": "thread", "created_at": 1719126964, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_3EX2cwlBKvkl6KBD6jIx3HlS", "object": "thread", "created_at": 1719127074, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_151AGboKqEk6eDRsmQWDMWr3", "object": "thread", "created_at": 1719127161, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_x6iu5GTiO5RYMbxpxEu4QWoB", "object": "thread", "created_at": 1719127387, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_raxmezQqH0XN8I96H18hNhot", "object": "thread", "created_at": 1719127462, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_rlEUn63EWVUglGGBxbjYzpnP", "object": "thread", "created_at": 1719127831, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_v78Bu9onmiVT56vwp6SG54ao", "object": "thread", "created_at": 1719128269, "metadata": {"action": "False"}, "tool_resources": {}}, 
#                 {"id": "thread_c7LnPGwfzSHFFnXxl0wW7DGZ", "object": "thread", "created_at": 1719128286, "metadata": {"action": "False"}, "tool_resources": {}}
#             ]
#         }
#     )
# )


# print(rec.retrieve_record('abhiteftest@gmail.com'))

