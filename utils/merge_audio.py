import cv2
from moviepy.editor import *


def add_audio_to_video(video_path, audio_path, output_path):
    # Read the video using OpenCV
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Read the audio using moviepy
    audio_clip = AudioFileClip(audio_path)

    # Combine the video and audio
    video_clip = VideoFileClip(video_path)
    video_clip = video_clip.set_audio(audio_clip)

    # Write the combined video to a new file
    video_clip.write_videofile(
        output_path, fps=fps, codec='libx264', audio_codec='aac', threads=4)

    # Release the video capture
    cap.release()

    print("Video with audio added successfully.")
