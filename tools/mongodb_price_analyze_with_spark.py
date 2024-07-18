from pyspark.sql import SparkSession
from pyspark.sql.functions import regexp_replace, col, avg, when
import pyspark.sql.functions as F
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

# Show the structure of the data
df.printSchema()
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
avg_price.show()

# Filter data based on a condition
# filtered_df = df.filter(df["price_cleaned"] > 10)
filtered_df = df.filter(df["area"] > 50)
# Show the filtered data
filtered_df.select("area", "price", "location", "title").show()

# EDA
# from pyspark.sql.functions import mean, min
#
# mean_value = df.select(mean(df['price_cleaned'])).collect()
# min_value = df.select(min(df['price_cleaned'])).collect()
#
# print("Mean value of price:", mean_value[0][0])
# print("Min value of price:", min_value[0][0])

# Calculate EDA value
total_count = df.count()
mean_value = df.agg(F.mean('price_cleaned')).collect()[0][0]
min_value = df.agg(F.min('price_cleaned')).collect()[0][0]
max_value = df.agg(F.max('price_cleaned')).collect()[0][0]
stddev_value = df.agg(F.stddev('price_cleaned')).collect()[0][0]
variance_value = df.agg(F.variance('price_cleaned')).collect()[0][0]
sum_value = df.agg(F.sum('price_cleaned')).collect()[0][0]
count_value = df.agg(F.count('price_cleaned')).collect()[0][0]
median_value = df.approxQuantile('price_cleaned', [0.5], 0.01)[0]
quantiles = df.approxQuantile('price_cleaned', [0.25, 0.5, 0.75], 0.01)
first_quartile = quantiles[0]
third_quartile = quantiles[2]
skewness_value = df.agg(F.skewness('price_cleaned')).collect()[0][0]
kurtosis_value = df.agg(F.kurtosis('price_cleaned')).collect()[0][0]
correlation_value = df.stat.corr('price_cleaned', 'area')
covariance_value = df.stat.cov('price_cleaned', 'area')
distinct_count_value = df.agg(F.approx_count_distinct('price_cleaned')).collect()[0][0]

# Print EDA values
print(f"Total number of real estate records: {total_count}")
print(f"Mean: {mean_value}")
print(f"Min: {min_value}")
print(f"Max: {max_value}")
print(f"Standard Deviation: {stddev_value}")
print(f"Variance: {variance_value}")
print(f"Sum: {sum_value}")
print(f"Count: {count_value}")
print(f"Median: {median_value}")
print(f"First Quartile: {first_quartile}")
print(f"Third Quartile: {third_quartile}")
print(f"Skewness: {skewness_value}")
print(f"Kurtosis: {kurtosis_value}")
print(f"Correlation with Area: {correlation_value}")
print(f"Covariance with Area: {covariance_value}")
print(f"Distinct Count: {distinct_count_value}")
# # Save the results to MongoDB
# avg_price_per_district.write.format("mongodb").mode("overwrite").option("database", "realestate").option("collection", "avg_price_per_district").save()
# df.select('area').toPandas().hist()

spark.stop()