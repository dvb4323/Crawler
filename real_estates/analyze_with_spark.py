from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, col, avg, expr

# Create Spark session
spark = SparkSession.builder \
    .appName("Real Estate Analysis") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/realestate.hanoi") \
    .config("spark.mongodb.output.uri", "mongodb://localhost:27017/realestate.hanoi") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0") \
    .getOrCreate()

# Read data from MongoDB
df = (spark.read.format("mongodb")
      .option("collection", "hanoi")
      .option("database", "realestate")
      .load())

# Show the data
df.show()

# Data cleaning
df = df.withColumn("price_cleaned", regexp_replace(col("price"), "Giá: ", ""))
df = df.withColumn("price_cleaned", regexp_replace(col("price_cleaned"), " tỷ", ""))
df = df.withColumn("price_cleaned", regexp_replace(col("price_cleaned"), ",", ".").cast("float"))

df = df.withColumn("area", regexp_replace(col("area"), " m²", "").cast("double"))

df = df.withColumn("district", regexp_replace(col("location"), ".*, Phường (.+?), Quận (.+?)", "$2"))

# Calculate average price per district
avg_price_per_district = df.groupBy("district").agg(avg("price_cleaned").alias("avg_price"))

# Show the results
avg_price_per_district.show()

# Save the results to MongoDB
avg_price_per_district.write.format("mongodb").mode("overwrite").option("database", "realestate").option("collection", "avg_price_per_district").save()
