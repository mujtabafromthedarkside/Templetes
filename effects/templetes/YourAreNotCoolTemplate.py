import cv2


def YourAreNotCoolTemplate(image_path, video_path, start_time, end_time, output_path):

    image = cv2.imread(image_path)

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

    for frame_number in range(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))):

        ret, frame = cap.read()

        if not ret:
            break

        if start_frame <= frame_number <= end_frame:
            if frame_number % 30 == 0:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
                # reshape image into frame
                image = cv2.resize(image, (frame_width, frame_height))
                # make alpha channel zero
                frame[:, :, 3] = 0
                print(image.shape, frame.shape, "image.shape, frame.shape")
                frame = cv2.addWeighted(frame, 0.5, image, 0.5, 0)
            else:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)
                # reshape image into frame
                image = cv2.resize(image, (frame_width, frame_height))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2BGRA)
                # make alpha channel zero
                image[:, :, 3] = 0
                print(image.shape, frame.shape, "image.shape, frame.shape")
                frame = cv2.addWeighted(frame, 0.5, image, 0.5, 0)

        output_video.write(frame)

    cap.release()
    output_video.release()
    cv2.destroyAllWindows()

    print("Circular translation video created successfully.")
