import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB connection string
database = client['real_estate_hanoi']  # Update with your database name

# # Function to search for documents with area containing dots
# def search_for_dotted_areas():
#     results = []
#     # Iterate through collections
#     for collection_name in database.list_collection_names():
#         collection = database[collection_name]
#         # Search for documents with area containing dots
#         query = {"area": {"$regex": r"\d+\.\d+"}}  # Matches numbers with dots (e.g., 10.300)
#         cursor = collection.find(query)
#         for doc in cursor:
#             results.append((collection_name, doc))
#     return results
#
# # Perform the search
# search_results = search_for_dotted_areas()
#
# # Print the results
# for collection_name, doc in search_results:
#     print(f"Collection: {collection_name}")
#     print(f"Document: {doc}")
#     print()
# Function to update documents to remove dots from the area field
def remove_dots_from_area():
    # Iterate through collections
    for collection_name in database.list_collection_names():
        collection = database[collection_name]
        # Update documents to remove dots from the area field
        query = {"area": {"$regex": r"\d+\.\d+"}}  # Matches numbers with dots (e.g., 10.300)
        cursor = collection.find(query)
        for doc in cursor:
            # Remove dots from the area value
            new_area = doc['area'].replace('.', '')
            # Update the document with the new area value
            update_query = {"_id": doc['_id']}
            update = {"$set": {"area": new_area}}
            collection.update_one(update_query, update)
            print(f"Updated document with _id {doc['_id']} in collection {collection_name}")

# Perform the update
remove_dots_from_area()