import pymongo
import pandas as pd
import re
from matplotlib import pyplot as plt

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB connection string
database = client['real_estate_hanoi']  # Update with your database name
collection = database['huyen_thuong_tin']  # Update with your collection name

# Fetch all documents from the collection
data = list(collection.find({}))

# Convert the MongoDB documents to a pandas DataFrame
df = pd.DataFrame(data)

# Print the DataFrame columns to check their names
print("DataFrame columns:", df.columns)

def convert_price(price_str):
    """
    Convert price strings to numeric values in billion VND.
    """
    if isinstance(price_str, str):
        price_str = price_str.replace(',', '').strip()
        if 'triệu' in price_str:
            return float(re.sub(r'[^\d.]', '', price_str)) / 1000  # Convert triệu to tỷ
        elif 'tỷ' in price_str or 'ty' in price_str:
            return float(re.sub(r'[^\d.]', '', price_str))
    return None

def convert_area(area_str):
    """
    Convert area strings to numeric values.
    """
    if isinstance(area_str, str):
        area_str = area_str.replace(' ', '').replace('m²', '').replace('m2', '')
        try:
            return float(area_str)
        except ValueError:
            return None
    return None

def clean_size(size_str):
    """
    Extract dimensions from size strings and convert to numeric.
    """
    if isinstance(size_str, str):
        match = re.findall(r'\d+\.\d+|\d+', size_str)
        return [float(num) for num in match] if match else None
    return None

def clean_road_before_width(width_str):
    """
    Convert road width strings to numeric values.
    """
    if isinstance(width_str, str):
        width_str = width_str.replace('m', '').replace(' ', '')
        try:
            return float(width_str)
        except ValueError:
            return None
    return None

# Check if the columns exist before applying functions
if 'price' in df.columns:
    df['price'] = df['price'].apply(convert_price)
    print("Prices after conversion:")
    print(df['price'])
else:
    print("Column 'price' not found in the DataFrame")

if 'area' in df.columns:
    df['area'] = df['area'].apply(convert_area)
    print("Area after conversion:")
    print(df['area'])
else:
    print("Column 'area' not found in the DataFrame")

if 'size' in df.columns:
    df['size'] = df['size'].apply(clean_size)
    print("Size after conversion:")
    print(df['size'])
else:
    print("Column 'size' not found in the DataFrame")

if 'road_before_width' in df.columns:
    df['road_before_width'] = df['road_before_width'].apply(clean_road_before_width)
    print("RBW after conversion:")
    print(df['road_before_width'])
else:
    print("Column 'road_before_width' not found in the DataFrame")

if 'floors' in df.columns:
    df['floors'] = pd.to_numeric(df['floors'], errors='coerce')
    print("Floors after conversion:")
    print(df['floors'])
else:
    print("Column 'floors' not found in the DataFrame")

if 'bedrooms' in df.columns:
    df['bedrooms'] = pd.to_numeric(df['bedrooms'], errors='coerce')
    print("Bedrooms after conversion:")
    print(df['bedrooms'])
else:
    print("Column 'bedrooms' not found in the DataFrame")

# Handle missing values if necessary
df.fillna({
    'floors': 0,
    'bedrooms': 0,
    'price': df['price'].median() if 'price' in df.columns and not df['price'].isnull().all() else 0,
    'area': df['area'].median() if 'area' in df.columns and not df['area'].isnull().all() else 0,
    'road_before_width': df['road_before_width'].median() if 'road_before_width' in df.columns and not df['road_before_width'].isnull().all() else 0
}, inplace=True)

# Use infer_objects to convert object types to the appropriate dtype
df = df.infer_objects()

# Set options to display more columns and rows
pd.set_option('display.max_columns', None)  # Display all columns
pd.set_option('display.max_rows', None)     # Display all rows
pd.set_option('display.max_colwidth', None) # No limit on column width
pd.set_option('display.width', 1000)

# Display the cleaned DataFrame
print("First few rows of the cleaned DataFrame:")
print(df.head())

# Display descriptive statistics
print("\nDescriptive statistics:")
print(df.describe(include='all'))

# Plot histogram using matplotlib
plt.figure(figsize=(10, 6))
plt.hist(df['price'], bins=20, edgecolor='black')
plt.xlabel('Price (ty)')
plt.ylabel('Frequency')
plt.title('Histogram of Property Prices')
plt.grid(True)
plt.show()

# Plot histogram for area using matplotlib
plt.figure(figsize=(10, 6))
plt.hist(df['area'], bins=20, edgecolor='black')
plt.xlabel('Area (m²)')
plt.ylabel('Frequency')
plt.title('Histogram of Property Areas')
plt.grid(True)
plt.show()

# Plot histogram for road_before_width using matplotlib
plt.figure(figsize=(10, 6))
plt.hist(df['road_before_width'], bins=10, edgecolor='black')
plt.xlabel('Road Before Width')
plt.ylabel('Frequency')
plt.title('Histogram of Road Before Width')
plt.grid(True)
plt.show()

# Filter out NaN values from 'floors' column
filtered_floors = df['floors'].dropna()

# Plot histogram using matplotlib
plt.figure(figsize=(8, 6))
plt.hist(filtered_floors, bins=5, edgecolor='black')
plt.xlabel('Floors')
plt.ylabel('Frequency')
plt.title('Histogram of Floors')
plt.grid(True)
plt.show()

# Filter out NaN values from 'floors' column
filtered_bedrooms = df['bedrooms'].dropna()

# Plot histogram using matplotlib
plt.figure(figsize=(8, 6))
plt.hist(filtered_bedrooms, bins=5, edgecolor='black')
plt.xlabel('Bedrooms')
plt.ylabel('Frequency')
plt.title('Histogram of Bedrooms')
plt.grid(True)
plt.show()

# Plotting using matplotlib
plt.figure(figsize=(8, 6))
plt.scatter(df['area'], df['price'], color='blue', alpha=0.5)
plt.title('Relationship between Area and Price')
plt.xlabel('Area (m²)')
plt.ylabel('Price (billion VND)')
plt.grid(True)
plt.show()