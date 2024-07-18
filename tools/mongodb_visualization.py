import pymongo
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Function to convert price from 'triệu' to 'tỷ'
def convert_price(price):
    if 'triệu' in price:
        value = float(price.replace(" triệu", ""))
        value = value / 1000  # Convert triệu to tỷ
    elif 'tỷ' in price:
        value = float(price.replace(" tỷ", ""))
    else:
        value = None
    return value
# Function to clean area value
# def clean_area(value):
#     value = value.replace('\xa0', '').replace('/', '').replace('m', '').strip()
#     return float(value) if value else None

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")  # Update with your MongoDB connection string
db = client['real_estate_hanoi']  # Update with your database name
collection = db['huyen_thuong_tin']  # Update with your collection name

# Read data from MongoDB
data = list(collection.find())

# Convert to DataFrame
df = pd.DataFrame(data)

# Preprocess the data
df['area'] = df['area'].str.replace(" m²", "").astype(float)
df['price'] = df['price'].apply(convert_price)

# Example visualizations

# Bar chart for floors and bedrooms
plt.figure(figsize=(10, 5))
sns.barplot(data=df[['floors', 'bedrooms']])
plt.title('Number of Floors and Bedrooms')
plt.show()

# Pie chart for parking
plt.figure(figsize=(5, 5))
df['parking'].value_counts().plot.pie(autopct='%1.1f%%')
plt.title('Parking Availability')
plt.show()

# Histogram for area
plt.figure(figsize=(10, 5))
sns.histplot(df['area'], bins=10)
plt.title('Distribution of Area')
plt.xlabel('Area (m²)')
plt.show()

# Histogram for price
plt.figure(figsize=(10, 5))
sns.histplot(df['price'], bins=10)
plt.title('Distribution of Price')
plt.xlabel('Price (tỷ)')
plt.show()

# Scatter plot for area vs price
plt.figure(figsize=(10, 5))
sns.scatterplot(x='area', y='price', data=df)
plt.title('Area vs Price')
plt.xlabel('Area (m²)')
plt.ylabel('Price (tỷ)')
plt.show()
