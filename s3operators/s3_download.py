"""
Download a video from S3
"""
import boto3
import botocore


video_name = 'raj-archery.mp4'
bucket = "human-action-recognition-bucket"
key = video_name
local_input_path = video_name
s3_client = boto3.client('s3')
try:
    s3_client.download_file(bucket, key, local_input_path)
    object = s3_client.head_object(Bucket=bucket, Key=key)
    print(f"Successfully downloaded object '{key}' from S3 bucket '{bucket}' to '{local_input_path}'.")
except botocore.exceptions.ClientError as e:
    print(f"Error downloading object '{key}' from S3 bucket '{bucket}': {str(e)}")
except s3_client.exceptions.LimitExceedException as e:
    print("API call limit exceeded")
    
