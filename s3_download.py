import boto3
import botocore


video_name = 'obj.txt'
bucket = "human-action-recognition-bucket"
key = "inputs/" + video_name
local_input_path = "tmp/" + video_name
s3_client = boto3.client('s3')
try:
    s3_client.download_file(bucket, key, local_input_path)
    object = s3_client.head_object(Bucket=bucket, Key=key)
    print(f"Successfully downloaded object '{key}' from S3 bucket '{bucket}' to '{local_input_path}'.")
    print(object)
    # metadata = object.metadata
    # print(f"object metadata '{metadata}'")
except botocore.exceptions.ClientError as e:
    print(f"Error downloading object '{key}' from S3 bucket '{bucket}': {str(e)}")
except s3_client.exceptions.LimitExceedException as e:
    print("API call limit exceeded")
    
