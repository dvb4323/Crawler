from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, col, avg, expr, when

# Create Spark session
spark = SparkSession.builder \
    .appName("Real Estate Analysis") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/real_estate_hanoi.huyen_thuong_tin") \
    .config("spark.mongodb.output.uri", "mongodb://localhost:27017/real_estate_hanoi.huyen_thuong_tin") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0") \
    .getOrCreate()

# Read data from MongoDB
df = (spark.read.format("mongodb")
      .option("collection", "huyen_thuong_tin")
      .option("database", "real_estate_hanoi")
      .load())

# Show the data
df.show()

# Data cleaning
# Data cleaning: convert "triệu" to "tỷ" and remove "tỷ"
df = df.withColumn(
    "price_cleaned",
    when(
        col("price").contains("triệu"),
        regexp_replace(col("price"), " triệu", "").cast("float") / 1000
    ).when(
        col("price").contains("tỷ"),
        regexp_replace(col("price"), " tỷ", "").cast("float")
    ).otherwise(None)
)

df = df.withColumn("area", regexp_replace(col("area"), " m²", "").cast("double"))

# Calculate average price per district
avg_price = df.agg(avg("price_cleaned").alias("avg_price"))

# Show the results
# avg_price.show()

# Filter data based on a condition
# filtered_df = df.filter(df["price_cleaned"] > 10)
filtered_df = df.filter(df["area"] > 50)
# Show the filtered data
filtered_df.select("area", "price", "location", "title").show()

# # Save the results to MongoDB
# avg_price_per_district.write.format("mongodb").mode("overwrite").option("database", "realestate").option("collection", "avg_price_per_district").save()
