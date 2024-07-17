import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB connection string
database = client['real_estate_hanoi']  # Update with your database name

# Function to search for documents with price '0.0 ty'
def search_for_zero_price():
    results = []
    # Iterate through collections
    for collection_name in database.list_collection_names():
        collection = database[collection_name]
        # Search for documents with price '0.0 ty'
        query = {"price": "0.0 tỷ"}
        cursor = collection.find(query)
        for doc in cursor:
            results.append((collection_name, doc))
    return results

# Perform the search
search_results = search_for_zero_price()

# Print the results
for collection_name, doc in search_results:
    print(f"Collection: {collection_name}")
    print(f"Document: {doc}")
    print()
