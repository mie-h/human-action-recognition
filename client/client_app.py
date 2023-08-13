import boto3
import botocore
import configparser
import json
import requests
import shutil
from fastapi import FastAPI

app = FastAPI()

config = configparser.ConfigParser()
config.read("config.ini")


@app.get("/")
def root():
    return {"welcome.": "client app"}


@app.get("/upload")
def upload_video(video_name: str):
    """Get presigned url and upload a video to S3 bucket
    Parameters
    ----------
    video_name : string
        path to the input video
    """
    lambda_client = boto3.client("lambda")

    # webhook url is your host url + /postprocessing
    # /postprocessing is defined below this function
    webhook_url = config.get("URL", "WEBHOOK_URL")
    payload = {"video_id": video_name, "webhook_url": webhook_url}

    # this API gateway endpoint should be publicly accessible
    apigateway_url = config.get("URL", "APIGATEWAY_URL")

    # get presigned url from API Gateway endpoint
    # field is necessary to upload a video successfully
    response = requests.get(apigateway_url, params=payload)
    print(f"Response: {response}")

    content = json.loads(response.text)
    url_s3presignedurl = content["payload"]["url"]
    fields = content["payload"]["fields"]
    print(f"Recieved s3 presigned url {url_s3presignedurl} and fields {fields}")

    # upload to the S3 bucket using presigned url
    local_video_path = video_name
    input_videos = {"file": open(local_video_path, "rb")}
    r = requests.post(url_s3presignedurl, data=fields, files=input_videos)

    print(f"status code of the upload to S3 bucket {r.status_code}")
    print(f"text of response from the upload to S3 bucket {r.text}")


@app.get("/postprocessing")
def post_processing(presignedurl: str):
    """Receives presigned url to download an output video from S3 and saves it to your local disk space.
    This endpoint is called by a service inside ECS task.
    Parameters
    ----------
    presignedurl : string
        s3 presigned url to download a video file
    """
    if not presignedurl:
        print("presigned url is empty")
        return
    print(f"Recieved presigned url {presignedurl}")
    print(f"Download an output video from S3 bucket")
    response = requests.get(presignedurl)
    if response.status_code == 200:
        with open(config.get("FILES", "OUTPUT_VIDEO_FILE"), "wb") as f:
            f.write(response.content)
        print("Downloading an output video succeeded")
    else:
        print("Downloading an output video failed")
        print(f"Status code: {response.status_code}")
