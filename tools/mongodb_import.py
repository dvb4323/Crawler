import os
import json
from pymongo import MongoClient
from pathlib import Path

def import_json_to_mongodb(json_dir, new_db_name, mongo_uri="mongodb://localhost:27017/"):
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client['real_estate_hanoi']

    # Iterate over each JSON file in the directory
    for file_name in os.listdir(json_dir):
        if file_name.endswith(".json"):
            collection_name = file_name[:-5]  # Remove .json extension to get collection name
            collection = db[collection_name]

            # Read JSON file
            with open(os.path.join(json_dir, file_name), "r", encoding="utf-8") as f:
                data = json.load(f)

                # Insert data into the collection
                if isinstance(data, list):
                    collection.insert_many(data)
                else:
                    collection.insert_one(data)

            print(f"Imported {file_name} to collection {collection_name}")

    client.close()

if __name__ == "__main__":
    # Define the directory containing JSON files
    json_dir = str(Path.home() / "Desktop" / "mongo_exports")

    # Define the new MongoDB database name
    new_db_name = "new_database_name"

    # Call the function to import JSON files
    import_json_to_mongodb(json_dir, new_db_name)
