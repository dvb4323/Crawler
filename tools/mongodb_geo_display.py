import pymongo
from opencage.geocoder import OpenCageGeocode
import folium

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB connection string
database = client['real_estate_hanoi']  # Update with your database name
collection_name = 'huyen_thuong_tin'  # Update with your collection name

# Function to fetch documents from MongoDB and merge location into a single string
def fetch_and_merge_location():
    geolocator = OpenCageGeocode('026fac41968e4347908dde446907ce2b')  # Replace with your OpenCage API key
    coordinates = []

    # Fetch documents from MongoDB collection
    collection = database[collection_name]
    cursor = collection.find({})

    for doc in cursor:
        if 'location' in doc and isinstance(doc['location'], list):
            # Merge location array into a single string
            location_string = ', '.join(doc['location'])

            # Geocode location string to get coordinates
            result = geolocator.geocode(location_string)
            if result and len(result):
                location_data = result[0]
                coordinates.append((location_string, location_data['geometry']['lat'], location_data['geometry']['lng']))
            else:
                print(f"Could not geocode location: {location_string}")

    return coordinates

# Get merged locations and geocode them
coordinates = fetch_and_merge_location()

# Create a folium map centered around the first location
if coordinates:
    map_center = coordinates[0][1], coordinates[0][2]
    mymap = folium.Map(location=map_center, zoom_start=12)  # Increased zoom level for better detail

    # Add markers for each location
    for location, lat, lon in coordinates:
        folium.Marker([lat, lon], popup=location).add_to(mymap)

    # Display the map
    mymap.save('map_opencage.html')  # Save the map as an HTML file
else:
    print("No valid coordinates found.")
