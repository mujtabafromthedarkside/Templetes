import cv2


def create_video_from_image(image_path, duration, fps, output_path):
    # Read the image
    image = cv2.imread(image_path)

    # Get image dimensions
    height, width, _ = image.shape

    # Create a video writer object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Choose the codec (e.g., mp4v)
    video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # Calculate the number of frames
    num_frames = int(fps * duration)

    # Write frames to the video
    for _ in range(num_frames):
        video_writer.write(image)

    # Release the video writer
    video_writer.release()

    print(f"Video saved to {output_path}.")


if __name__ == "__main__":
    create_video_from_image("/home/pydashninja/templetes/1.jpg",
                            10, 30, "/home/pydashninja/templetes/video.mp4")
    print("here")
