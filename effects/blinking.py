import cv2


def apply_blinking_effect(input_video_path, start_time, end_time, output_video_path):
    # Open the video file
    video = cv2.VideoCapture(input_video_path)

    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Calculate frame indices for start and end times
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Choose the codec (e.g., mp4v)
    video_writer = cv2.VideoWriter(
        output_video_path, fourcc, fps, (frame_width, frame_height))

    # Read and write each frame with blinking effect applied
    for frame_index in range(total_frames):
        ret, frame = video.read()

        if start_frame <= frame_index <= end_frame:
            # Apply blinking effect
            if (frame_index // int(fps/10)) % 2 == 0:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

        # Write the modified frame to the output video
        video_writer.write(frame)

    # Release the video capture and writer objects
    video.release()
    video_writer.release()

    print(f"Modified video saved to {output_video_path}.")


if __name__ == "__main__":
    apply_blinking_effect("/home/pydashninja/templetes/video.mp4",
                          0, 10, "/home/pydashninja/templetes/video2.mp4")
    print("here")
