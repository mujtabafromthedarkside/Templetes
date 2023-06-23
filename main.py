import moviepy.editor as mp
import cv2
import numpy as np
import random


def apply_filter(image, filter_type):
    # Apply different filters based on the filter_type
    if filter_type == 'grayscale':
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    elif filter_type == 'blur':
        return cv2.blur(image, (10, 10))
    elif filter_type == 'edges':
        return cv2.Canny(image, 100, 200)
    else:
        return image


def inference():
    input_image_path = '/home/pydashninja/templetes/1.jpg'

    # Output video path
    output_video_path = '/home/pydashninja/templetes/video.mp4'

    # Set video codec and properties
    codec = cv2.VideoWriter_fourcc(*'mp4v')
    fps = 30.0

    # Read the input image
    input_image = cv2.imread(input_image_path)
    output_size = (input_image.shape[1], input_image.shape[0])

    # Apply filters and effects
    filters = ['grayscale', 'blur']  # List of filters to apply

    # Repeat the filters list
    filters = filters * 3

    duration_per_filter = 3  # Duration (in seconds) for each filter

    # Initialize the video writer
    video_writer = cv2.VideoWriter(output_video_path, codec, fps, output_size)

    # Apply each filter and write frames to the video
    for filter_type in filters:
        # Apply the filter
        print("here2")
        filtered_image = apply_filter(input_image, filter_type)
        cv2.imwrite(
            f"/home/pydashninja/templetes/{filter_type}.jpg", filtered_image)

        # Check the type of filtered_image and convert it to RGB
        if filter_type == 'edges' or filter_type == 'grayscale':
            filtered_image = cv2.cvtColor(filtered_image, cv2.COLOR_GRAY2RGB)

        # Repeat frames for the desired duration
        num_frames = int(fps * duration_per_filter)
        for frame_idx in range(num_frames):
            # Add blinking effect
            if (frame_idx % 20) < 10:
                # Move image in and out effect using OpenCV
                if random.randint(0, 3) == 1:
                    # Calculate the scaling factor for zoom effect
                    # Increase scale linearly with frame number
                    scale = 1.0 + (frame_idx / num_frames)
                    scaled_image = cv2.resize(
                        filtered_image, None, fx=scale, fy=scale)

                    # Calculate the translation amount for panning effect
                    # Translate by 100 pixels linearly with frame number
                    translation = (frame_idx / num_frames) * 100
                    M = np.float32([[1, 0, translation], [0, 1, translation]])

                    # Apply the panning effect to the scaled image
                    panned_image = cv2.warpAffine(
                        scaled_image, M, (output_size[0], output_size[1]))

                    video_writer.write(panned_image)
                else:
                    video_writer.write(filtered_image)
            else:
                # Create water-like animation by adding random fluctuations
                water_image = np.zeros_like(filtered_image, dtype=np.float32)
                for i in range(filtered_image.shape[0]):
                    for j in range(filtered_image.shape[1]):
                        offset = random.randint(-3, 3)
                        water_image[i, j] = filtered_image[i,
                                                           (j + offset) % filtered_image.shape[1]]

                video_writer.write(water_image.astype(np.uint8))

    # Release the video writer and close the video file
    video_writer.release()
    cv2.destroyAllWindows()

    # read the video, add audio, and save it

    my_clip = mp.VideoFileClip(output_video_path)

    # set duration from 50 sec to depend on video duration

    audio_background = mp.AudioFileClip(
        "Kadi Te Has Bol Ve Manan Bhardwaj 320 Kbps.mp3").set_duration(my_clip.duration)

    final_clip = my_clip.set_audio(audio_background)

    final_clip.write_videofile("/home/pydashninja/templetes/final.mp4")


if __name__ == "__main__":
    inference()
