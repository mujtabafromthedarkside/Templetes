import cv2
import numpy as np


def switch_images_with_vibration(video_path, start_time, end_time, output_path, images_list):
    cap = cv2.VideoCapture(video_path)
    frame_rate = cap.get(cv2.CAP_PROP_FPS)
    start_frame = int(start_time * frame_rate)
    end_frame = int(end_time * frame_rate)

    images = [cv2.imread(img_path) for img_path in images_list]
    # resize all images to 1 image size
    images = [cv2.resize(img, (int(cap.get(3)), int(cap.get(4))))
              for img in images]

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, frame_rate,
                          (int(cap.get(3)), int(cap.get(4))))

    current_frame = 0
    switch_frame_interval = int(frame_rate)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if current_frame >= start_frame and current_frame <= end_frame:
            vibration_intensity = 10  # Adjust the vibration intensity as needed

            if current_frame % switch_frame_interval == 0:
                current_image_index = (
                    current_frame // switch_frame_interval) % len(images)
                # print("index", current_image_index)
                frame = images[current_image_index]

            rows, cols, _ = frame.shape
            dx = vibration_intensity * np.sin(2 * np.pi * current_frame / 100)
            dy = vibration_intensity * np.cos(2 * np.pi * current_frame / 100)

            M = np.float32([[1, 0, dx], [0, 1, dy]])
            frame = cv2.warpAffine(
                frame, M, (cols, rows), borderMode=cv2.BORDER_REPLICATE)

        out.write(frame)
        current_frame += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()
