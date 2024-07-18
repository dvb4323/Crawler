import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
database = client['real_estate_hanoi']  # Replace 'your_database' with your database name

# Get all collection names in the database
collection_names = database.list_collection_names()

# Define the update operation for 'parking' field
update_operations = [
    {'$set': {'parking': 1}},  # Set 'parking' to 1 if it's True
    {'$set': {'parking': 0}}   # Set 'parking' to 0 if it's False
]

# Iterate through each collection and perform update
for collection_name in collection_names:
    collection = database[collection_name]

    # Update where 'parking' is True
    filter_criteria_true = {'parking': True}
    update_operation_true = {'$set': {'parking': 1}}
    collection.update_many(filter_criteria_true, update_operation_true)

    # Update where 'parking' is False
    filter_criteria_false = {'parking': False}
    update_operation_false = {'$set': {'parking': 0}}
    collection.update_many(filter_criteria_false, update_operation_false)

print("Updates completed for all collections.")
