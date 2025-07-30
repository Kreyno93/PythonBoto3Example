import boto3
from botocore.exceptions import ClientError

# List all bucket in eu-central-1


def list_buckets():
    s3 = boto3.client("s3", region_name="eu-central-1")
    response = s3.list_buckets()
    for bucket in response["Buckets"]:
        print(f'Bucket Name: {bucket["Name"]}')


list_buckets()
