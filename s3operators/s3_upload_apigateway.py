"""
Upload a video file to S3 by url provided by API Gateway. 
API Gateway endpoint is open to public.
"""
import requests
import json
import boto3
import botocore

lambda_client = boto3.client("lambda")

# this part must be replaced with API Gateway call
video_name = "raj-bb.mp4"
url_s3presignedurl = f"https://yh89nuinqe.execute-api.us-west-1.amazonaws.com/prod/getpresignedurl?video_id={video_name}"

response = requests.get(url_s3presignedurl)

content = json.loads(response.text)
print(content["url"])
url_s3bucket = content["url"]["url"]
fields = content["url"]["fields"]

local_video_path = video_name
input_videos = {"file": open(local_video_path, "rb")}
r = requests.post(url_s3bucket, data=fields, files=input_videos)

print(r.status_code)
print(r.text)