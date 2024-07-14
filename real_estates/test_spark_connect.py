from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("MongoSparkConnectorIntro") \
    .config("spark.mongodb.input.uri", "mongodb://localhost:27017/realestate.hanoi") \
    .config("spark.mongodb.output.uri", "mongodb://localhost:27017/realestate.hanoi") \
    .config("spark.jars.packages", "org.mongodb.spark:mongo-spark-connector_2.12:10.3.0") \
    .getOrCreate()

df = (spark.read.format("mongodb")
      .option("collection", "hanoi")
      .option("database", "realestate")
      .load()
      )
df.show()
