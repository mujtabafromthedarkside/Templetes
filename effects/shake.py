import cv2
import numpy as np


def shake(video_path, start_time, end_time, output_path, shake_intensity=20, zoom_factor=1.2):
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
    is_shaking = True
    check = start_frame + int(fps)
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if is_shaking and start_frame <= cap.get(cv2.CAP_PROP_POS_FRAMES) <= end_frame:
            # Zoom-in effect: Resize the frame to larger dimensions
            new_width = int(frame_width * zoom_factor)
            new_height = int(frame_height * zoom_factor)
            zoomed_frame = cv2.resize(frame, (new_width, new_height))

            # Calculate a new random displacement for the shake effect
            dx, dy = np.random.randint(-shake_intensity,
                                       shake_intensity, size=2)

            # Translate the zoomed frame by the displacement
            translation_matrix = np.float32([[1, 0, dx], [0, 1, dy]])
            translated_frame = cv2.warpAffine(
                zoomed_frame, translation_matrix, (new_width, new_height))

            # Crop the result to the original size (to remove black borders)
            start_x, start_y = max(0, dx), max(0, dy)
            end_x, end_y = min(new_width, frame_width +
                               dx), min(new_height, frame_height + dy)
            cropped_frame = translated_frame[start_y:start_y +
                                             frame_height, start_x:start_x + frame_width]
            output_video.write(cropped_frame)
        else:
            output_video.write(frame)

        # Check if we have reached the end time for each shaking interval
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == check:
            is_shaking = not is_shaking

            # Skip 1 second for the non-shaking period
            check += int(fps)

    # Release the video reader and writer
    cap.release()
    output_video.release()
    cv2.destroyAllWindows()

    print("Shaking video created successfully.")
