# Human Action Recognition

A service that predicts human action in a video using pre-trained PyTorch models. Deployed on AWS Cloud using ECS, S3, EventBridge, and lambda. 

<!-- Example output 1: basketball

video here
need to reduce the video size

Example output 2: archery

video here
need to reduce the video size -->


# How It Works

Get S3 presigned URL with from API Gateway, and upload an input video to S3 bucket using the presigned URL.

![](images/HAR_phase1.drawio.png)


Put operation on S3 is logged with CloudTrail. Eventbridge rule recognizes the put object log and starts a new ECS task.

![](images/HAR_phase2.drawio.png)

The triggered and initialized ECS task does the human action recognition prediction using pre-trained Pytorch model, and saves the output to S3 bucket. 

![](images/HAR_phase3.drawio.png)


# Usage

I implemented [a simple client side code](https://github.com/mie-h/human-action-recognition/blob/main/client/client_app.py) using FastAPI. Please refer to this page for how to use this service. 


# Thoughts and Optimization

<!-- free campus. be as creative as you want :D -->

- Both input and output videos are saved in the same S3 bucket. For the EventBridge rule on S3 PUT OBJECT, input and output videos should be in the separate buckets to avoid infinite cycle for the best practice.
<!-- * thoughts on Volume/Scale/QPS/latency -->

# Things I learned
* [Passing S3 PutObject event data to ECS task](https://github.com/mie-h/passing-event-data-ecs-task/tree/main)
* [multipart upload + presigned url](https://github.com/mie-h/multipart-upload-presignedurl)



# Acknowledgments

* [Human Action Recognition in Videos using PyTorch](https://debuggercafe.com/human-action-recognition-in-videos-using-pytorch/)
