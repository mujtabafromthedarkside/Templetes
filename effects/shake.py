import cv2
import numpy as np

# Replace 'your_image_path.jpg' with the actual path of your image


def shake(video_path, start_time, end_time, output_path, shake_intensity=15):
    # Read the input video
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate frame numbers for start and end time
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Create the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(
        output_path, fourcc, fps, (frame_width, frame_height))

    # Process video frames
    frame_number = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_number >= start_frame and frame_number <= end_frame:
            # Compute the displacement for the shake effect
            dx, dy = np.random.randint(-shake_intensity,
                                       shake_intensity, size=2)

            # Translate the frame by the displacement
            M = np.float32([[1, 0, dx], [0, 1, dy]])
            translated_frame = cv2.warpAffine(
                frame, M, (frame_width, frame_height))
            output_video.write(translated_frame)
        else:
            output_video.write(frame)

        frame_number += 1

    # Release the video reader and writer
    cap.release()
    output_video.release()
    cv2.destroyAllWindows()

    print("Shaking video created successfully.")
