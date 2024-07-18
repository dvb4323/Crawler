from pymongo import MongoClient

# Replace the following with your MongoDB connection details
mongo_uri = "mongodb://localhost:27017/"
database_name = "real_estate_hanoi"
collection_name = "huyen_thuong_tin"

# Connect to the MongoDB server
client = MongoClient(mongo_uri)

# Access the database and collection
db = client[database_name]
collection = db[collection_name]

# Define the search value
search_value = '1.35 tỷ /\xa0m'
new_value = '1.35 tỷ'
# Function to build regex query for each field
def build_field_queries(search_value):
    queries = []
    fields = collection.find_one().keys()
    for field in fields:
        if field != "_id":  # Skip the _id field
            queries.append({field: {"$regex": search_value}})
    return queries

# Build the query
field_queries = build_field_queries(search_value)
query = {"$or": field_queries}


# Find the matching documents
matching_documents = collection.find(query)

# Update the matching documents
for doc in matching_documents:
    updated_fields = {}
    for field in doc:
        if isinstance(doc[field], str) and search_value in doc[field]:
            updated_fields[field] = doc[field].replace(search_value, new_value)
    if updated_fields:
        collection.update_one({"_id": doc["_id"]}, {"$set": updated_fields})

print("Update completed.")

# Print matching documents
print("Matching documents:")
for doc in matching_documents:
    print(doc)

# Close the MongoDB connection
client.close()
