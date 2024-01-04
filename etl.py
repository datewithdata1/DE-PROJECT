import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue import DynamicFrame
import boto3
import os

# Specify your S3 bucket and path
bucket_name = 'project-de-datewithdata'
prefix = 'warehouse/'

# Initialize S3 client
s3 = boto3.client('s3')


def sparkUnion(glueContext, unionType, mapping, transformation_ctx) -> DynamicFrame:
    # Check if any of the frames in the mapping is empty
    if any(frame.count() == 0 for alias, frame in mapping.items()):
        # If any frame is empty, return the non-empty frame
        non_empty_frame = next(frame for alias, frame in mapping.items() if frame.count() > 0)
        return non_empty_frame
    else:
        # All frames are non-empty, perform the union
        for alias, frame in mapping.items():
            frame.toDF().createOrReplaceTempView(alias)
        result = spark.sql(
            "(select * from {}) UNION {} (select * from {})".format(*mapping.keys())
        )
        return DynamicFrame.fromDF(result, glueContext, transformation_ctx)


args = getResolvedOptions(sys.argv, ["JOB_NAME"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script  for node Mark
Mark_node1704390766767 = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": '"', "withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={
        "paths": ["s3://project-de-datewithdata/staging/mark/"],
        "recurse": True,
    },
    transformation_ctx="Mark_node1704390766767",
)
print("Read Mark Data")


# Script for node Student
Student_node1704390766920 = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": '"', "withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={
        "paths": ["s3://project-de-datewithdata/staging/student/"],
        "recurse": True,
    },
    transformation_ctx="Student_node1704390766920",
)
print("Read Student Data")

# Script for node DW
DW_node1704390869493 = glueContext.create_dynamic_frame.from_options(
    format_options={"quoteChar": '"', "withHeader": True, "separator": ","},
    connection_type="s3",
    format="csv",
    connection_options={
        "paths": ["s3://project-de-datewithdata/warehouse/"],
        "recurse": True,
    },
    transformation_ctx="DW_node1704390869493",
)
print("Read DW Data")

# Script  for node Join
Join_node1704390823387 = Join.apply(
    frame1=Mark_node1704390766767,
    frame2=Student_node1704390766920,
    keys1=["student_id"],
    keys2=["id"],
    transformation_ctx="Join_node1704390823387",
)
print("Join Sucessful")

# Script  for node Union
Union_node1704390896227 = sparkUnion(
    glueContext,
    unionType="ALL",
    mapping={"source1": Join_node1704390823387, "source2": DW_node1704390869493},
    transformation_ctx="Union_node1704390896227",
)

print("Union Sucessful")

# List all objects in the specified S3 path
objects = s3.list_objects(Bucket=bucket_name, Prefix=prefix)['Contents']

# Delete each object
for obj in objects:
    s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
print("Delete existing files") 
    

AmazonS3_node1704390958322 = glueContext.write_dynamic_frame.from_options(
    frame=Union_node1704390896227,
    connection_type="s3",
    format="glueparquet",
    connection_options={
        "path": "s3://project-de-datewithdata/warehouse/",
        "partitionKeys": [],
    },
    format_options={"compression": "snappy"},
    transformation_ctx="AmazonS3_node1704390958322",
)
print("Save the data")
job.commit()
