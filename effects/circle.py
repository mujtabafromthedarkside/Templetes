import cv2
import numpy as np


def translate_in_circle(video_path, start_time, end_time, output_path, radius=2):
    # Read the input video
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Calculate frame numbers for start and end time
    print("fps", fps, "start_time", start_time, "end_time", end_time,
          "frame_width", frame_width, "frame_height", frame_height)

    start_frame = int(start_time * int(fps))
    end_frame = int(end_time * int(fps))
    # print("start_frame", start_frame, "end_frame", end_frame,
    #       "middle_frame", (start_frame - end_frame)/2)

    # Create the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(
        output_path, fourcc, fps, (frame_width, frame_height))

    # Process video frames with circular translation
    udpate_image = False
    check1 = True
    for frame_number in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):
        if not udpate_image:
            # print("not updated")
            ret, frame = cap.read()
        else:
            # print("here")
            ret, _ = cap.read()

        if not ret:
            break

        if frame_number == int(start_frame + 15):
            if check1 == True:
                print("frame_number", frame_number)
            frame = cv2.imread("2.jpg")
            frame = cv2.resize(frame, (frame_width, frame_height))
            check1 = False
            # make it grey scale
            # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            udpate_image = True

        if start_frame <= frame_number <= end_frame:
            # Calculate the angle for the circular translation
            if frame_number >= end_frame:
                udpate_image = False
            angle = 30 * np.pi * (frame_number - start_frame) / \
                (end_frame - start_frame)

            # Calculate the new center position based on the angle and radius
            center_x, center_y = frame_width // 2, frame_height // 2
            new_center_x = center_x + int(radius * np.cos(angle))
            new_center_y = center_y + int(radius * np.sin(angle))

            # Create the transformation matrix for the circular translation
            M = np.float32([[1, 0, new_center_x - center_x],
                           [0, 1, new_center_y - center_y]])

            # Apply the transformation to the frame
            translated_frame = cv2.warpAffine(
                frame, M, (frame_width, frame_height), borderMode=cv2.BORDER_REPLICATE)

            # Write the frame to the output video
            output_video.write(translated_frame)
        else:
            # print("Frame number", frame_number, "not in range")
            # Write the original frame to the output video
            output_video.write(frame)

    # Release the video reader and writer
    cap.release()
    output_video.release()
    cv2.destroyAllWindows()

    print("Circular translation video created successfully.")
