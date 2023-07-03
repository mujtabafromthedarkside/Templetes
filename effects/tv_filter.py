import cv2
import numpy as np


import cv2
import numpy as np


def tv_filter(video_path, start_time, output_time, output_path):
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate start and end frame numbers
    start_frame = int(start_time * fps)
    end_frame = int(output_time * fps)

    # Create VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps,
                          (frame_width, frame_height))

    # Loop through the frames and apply the effect
    frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Apply the effect only within the specified interval
        if start_frame <= frame_num <= end_frame:
            # Convert to grayscale
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Apply noise
            noise = np.random.normal(0, 1, gray.shape).astype(np.uint8)
            gray = cv2.add(gray, noise)

            # Increase contrast
            gray = cv2.equalizeHist(gray)

            # Convert back to color
            frame = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        # Write the modified frame to the output video
        out.write(frame)

        frame_num += 1

    # Release the resources
    cap.release()
    out.release()

    print("The 1950s effect has been applied, and the output video is saved at:", output_path)


if __name__ == "__main__":
    tv_filter("/home/pydashninja/templetes/video.mp4",
              0, 10, "/home/pydashninja/templetes/video2.mp4")
    print("here")
