import os
import json
from pymongo import MongoClient
from pathlib import Path


def export_collections_to_json(db_name, output_dir, mongo_uri="mongodb://localhost:27017"):
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client['real_estate_hanoi']

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Iterate over each collection in the database
    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        data = list(collection.find())

        # Convert MongoDB documents to JSON-serializable format
        for document in data:
            document['_id'] = str(document['_id'])

        # Define output file path
        output_file = os.path.join(output_dir, f"{collection_name}.json")

        # Write data to JSON file
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"Exported {collection_name} to {output_file}")

    client.close()


if __name__ == "__main__":
    # Define your MongoDB database name
    db_name = "your_database_name"

    # Get the desktop path
    desktop_path = str(Path.home() / "Desktop")

    # Define the output directory on the desktop
    output_dir = os.path.join(desktop_path, "mongo_exports")

    # Call the function to export collections
    export_collections_to_json(db_name, output_dir)
