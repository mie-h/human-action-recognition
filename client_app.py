import boto3
import botocore
import json
import requests
import shutil
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"welcome.": "client app"}


@app.get("/upload")
def upload_video():
    lambda_client = boto3.client("lambda")

    # this part must be replaced with API Gateway call
    video_name = "raj-bb.mp4"
    webhook_url = "http://127.0.0.1:8000/postprocessing"
    payload = {"video_id": video_name, "webhook_url": webhook_url}
    url_apigateway = f"https://yh89nuinqe.execute-api.us-west-1.amazonaws.com/prod/getpresignedurl"

    response = requests.get(url_apigateway, params=payload)
    print(response)

    content = json.loads(response.text)
    print(content["url"])
    url_s3presignedurl = content["url"]["url"]
    fields = content["url"]["fields"]

    local_video_path = video_name
    input_videos = {"file": open(local_video_path, "rb")}
    r = requests.post(url_s3presignedurl, data=fields, files=input_videos)

    print(r.status_code)
    print(r.text)


@app.get("/postprocessing")
def post_processing(presignedurl: str):
    if not presignedurl:
        print("presigned url is empty")
        return
    print(f"Recieved presigned url {presignedurl}")
    response = requests.get(presignedurl)
    if response.status_code == 200:
        with open("client_output.mp4", "wb") as f:
            f.write(response.content) 