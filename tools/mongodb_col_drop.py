import pymongo

def drop_multiple_collections(client, collection_names):
  """Drops multiple collections in a MongoDB database.

  Args:
    client: A pymongo MongoClient instance.
    collection_names: A list of collection names to drop.
  """

  for collection_name in collection_names:
    db = client[collection_name.split('.')[0]]  # Extract database name
    collection = db[collection_name.split('.')[1]]  # Extract collection name
    try:
      collection.drop()
      print(f"Collection '{collection_name}' dropped successfully.")
    except pymongo.errors.CollectionDoesNotExist:
      print(f"Collection '{collection_name}' does not exist.")

if __name__ == "__main__":
  # Replace with your MongoDB connection string
  client = pymongo.MongoClient("mongodb://localhost:27017/")

  # List of collection names to drop (adjust as needed)
  collection_names = ["real_estate_hanoi.quan_ba_dinh.html", "real_estate_hanoi.quan_cau_giay.html"]

  drop_multiple_collections(client, collection_names)
