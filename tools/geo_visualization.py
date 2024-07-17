from geopy.geocoders import Nominatim
import folium

# Example location data
locations = ['Tam Hiệp, Thanh Trì, Hà Nội', 'Tạ Quang Bửu, Hai Bà Trưng, Hà Nội', 'Quận 1, Hồ Chí Mình']

# Geocoding function to convert location names to coordinates
def geocode_locations(locations):
    geolocator = Nominatim(user_agent="chrome")
    coordinates = []
    for location in locations:
        location_data = geolocator.geocode(location)
        if location_data:
            coordinates.append((location, location_data.latitude, location_data.longitude))
        else:
            print(f"Could not geocode location: {location}")
    return coordinates

# Get coordinates for each location
coordinates = geocode_locations(locations)

# Create a folium map centered around the first location
map_center = coordinates[0][1], coordinates[0][2]
mymap = folium.Map(location=map_center, zoom_start=4)

# Add markers for each location
for location, lat, lon in coordinates:
    folium.Marker([lat, lon], popup=location).add_to(mymap)

# Display the map
mymap.save('map2.html')  # Save the map as an HTML file
