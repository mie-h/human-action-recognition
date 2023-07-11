import requests
import json
import boto3
import botocore

lambda_client = boto3.client("lambda")

function_name = "GeneratePresignURL"
video_name = "obj.txt"
function_params = {"video_id": video_name}
try:
    response = lambda_client.invoke(
        FunctionName=function_name, Payload=json.dumps(function_params)
    )
    print("Invoked function %s.", function_name)
except botocore.exceptions.ClientError as error:
    print("Couldn't invoke function %s.", function_name)
    raise

print(response["StatusCode"])

payload = eval(response["Payload"].read().decode("utf-8"))
print(payload)

# hwo to add metadata to s3 object when I upload
local_video_path = "./input/" + video_name
input_videos = {"file": open(local_video_path, "rb")}
r = requests.post(payload["url"], data=payload["fields"], files=input_videos)

print(r.status_code)
print(r.text)
