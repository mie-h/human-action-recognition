import torch
import torchvision
import cv2
import argparse
import time
import numpy as np
import utils




def action_recognition(input, local_dir="./", clip_len=16):

    # get the lables
    class_names = utils.class_names
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    # load the model
    model = torchvision.models.video.r3d_18(pretrained=True, progress=True)
    # load the model onto the computation device
    model = model.eval().to(device)

    cap = cv2.VideoCapture(input)
    if cap.isOpened() == False:
        print("Error while trying to read video. Please check path again")
    # get the frame width and height
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))

    save_name = f"{input.split('/')[-1].split('.')[0]}"
    # define codec and create VideoWriter object
    out = cv2.VideoWriter(
        f"{local_dir}{save_name}-output.mp4",
        cv2.VideoWriter_fourcc(*"mp4v"),
        30,
        (frame_width, frame_height),
    )

    frame_count = 0  # to count total frames
    total_fps = 0  # to get the final frames per second
    # a clips list to append and store the individual frames
    clips = []

    frame_count = 0  # to count total frames
    total_fps = 0  # to get the final frames per second
    # a clips list to append and store the individual frames
    clips = []

    # read until end of video
    while cap.isOpened():
        # capture each frame of the video
        ret, frame = cap.read()
        if ret == True:
            # get the start time
            start_time = time.time()
            image = frame.copy()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = utils.transform(image=frame)["image"]
            clips.append(frame)
            if len(clips) == clip_len:
                with torch.no_grad():  # we do not want to backprop any gradients
                    input_frames = np.array(clips)
                    # add an extra dimension
                    input_frames = np.expand_dims(input_frames, axis=0)
                    # transpose to get [1, 3, num_clips, height, width]
                    input_frames = np.transpose(input_frames, (0, 4, 1, 2, 3))
                    # convert the frames to tensor
                    input_frames = torch.tensor(input_frames, dtype=torch.float32)
                    input_frames = input_frames.to(device)
                    # forward pass to get the predictions
                    outputs = model(input_frames)
                    # get the prediction index
                    _, preds = torch.max(outputs.data, 1)

                    # map predictions to the respective class names
                    label = class_names[preds].strip()
                # get the end time
                end_time = time.time()
                # get the fps
                fps = 1 / (end_time - start_time)
                # add fps to total fps
                total_fps += fps
                # increment frame count
                frame_count += 1
                wait_time = max(1, int(fps / 4))
                cv2.putText(
                    image,
                    label,
                    (50, 50),
                    cv2.FONT_HERSHEY_DUPLEX,
                    0.8,
                    (125, 246, 55),
                    2,
                    lineType=cv2.LINE_AA,
                )
                clips.pop(0)
                out.write(image)
        else:
            break


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="path to input video")
    parser.add_argument(
        "-c",
        "--clip-len",
        dest="clip_len",
        default=16,
        type=int,
        help="number of frames to consider for each prediction",
    )
    args = vars(parser.parse_args())
 
    print(f"Number of frames to consider for each prediction: {args['clip_len']}")
    action_recognition(args["input"])

if __name__ == "__main__":
    main()