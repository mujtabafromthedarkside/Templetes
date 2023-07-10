import cv2
import os
import numpy as np

def effect(video_path, start_time, end_time, output_path):
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate start and end frame numbers
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Create VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps,
                          (frame_width, frame_height))
 
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Apply the effect only within the specified interval
        if start_frame <= frame_num <= end_frame:
            pass

        # Write the modified frame to the output video
        out.write(frame)
        frame_num += 1

    # Release the resources
    cap.release()
    out.release()

    print("The __ effect has been applied, and the output video is saved at:", output_path)
