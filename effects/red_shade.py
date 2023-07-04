import cv2


def create_red_box_animation(video_path, start_time, end_time, output_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Get the video's frame rate and dimensions
    fps = video.get(cv2.CAP_PROP_FPS)
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate the start and end frame numbers based on the given start and end times
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Define the red color (BGR) with 50% opacity
    red = (0, 0, 255)
    opacity = 0.2

    # Create a VideoWriter object to save the output video
    # Specify the codec (e.g., 'XVID', 'mp4v', 'MJPG')
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Loop through the frames of the video
    frame_number = 0
    while True:
        # Read the current frame
        ret, frame = video.read()

        # If the frame was not read successfully, break the loop
        if not ret:
            break

        # Check if the current frame is within the start and end frame range
        if start_frame <= frame_number <= end_frame:
            # Calculate the box height based on the current frame number
            box_height = int(
                height * (frame_number - start_frame) / (end_frame - start_frame))

            # Create a copy of the frame
            frame_copy = frame.copy()

            # Create a red box image with the same dimensions as the frame
            red_box = frame_copy.copy()
            red_box[:box_height, :] = red

            # Blend the red box with the frame using the opacity
            blended_frame = cv2.addWeighted(
                frame_copy, 1 - opacity, red_box, opacity, 0)

            # Add the blended frame to the output video
            output_video.write(blended_frame)
        else:
            # Add the original frame to the output video
            output_video.write(frame)

        # Increment the frame number
        frame_number += 1

    # Release the video capture and video writer objects
    video.release()
    output_video.release()


if __name__ == "__main__":
    create_red_box_animation("/home/pydashninja/templetes/video2.mp4",
                             0, 10, "/home/pydashninja/templetes/video3.mp4")
    print("here")
