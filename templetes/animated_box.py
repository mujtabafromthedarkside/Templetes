import cv2
import numpy as np

def animated_box(video_path, start_time, end_time, output_path):
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate start and end frame numbers
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Create VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps,
                          (frame_width, frame_height))
    
    # sprite = rounded box, in this function
    sprite = cv2.imread('subscribe2.png', cv2.IMREAD_UNCHANGED)

    # Loop through the frames and apply the effect
    frame_num = 0
    MAXSIZE = 150

    SIZE = 0
    ANGLE = 90

    SIZE_CHANGE = 2
    ANGLE_CHANGE = 2
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Apply the effect only within the specified interval
        if start_frame <= frame_num <= end_frame:
            # Calculate the position to place the second image in the middle of the first image
            resized_sprite = cv2.resize(sprite, (SIZE,SIZE))

            frame_x = (frame.shape[1] - resized_sprite.shape[1]) // 2
            frame_y = (frame.shape[0] - resized_sprite.shape[0]) // 2

            sprite_x = resized_sprite.shape[1] // 2
            sprite_y = resized_sprite.shape[0] // 2

            rotMatrix = cv2.getRotationMatrix2D((sprite_x, sprite_y), ANGLE, 1.0)
            resized_sprite = cv2.warpAffine(resized_sprite, rotMatrix, (resized_sprite.shape[1], resized_sprite.shape[0]))

            # Overlay the second image onto the first image
            for c in range(0, 3):
                frame[frame_y:frame_y+resized_sprite.shape[0], frame_x:frame_x+resized_sprite.shape[1], c] = resized_sprite[:, :, c] * (resized_sprite[:, :, 3] / 255.0) + frame[frame_y:frame_y+resized_sprite.shape[0], frame_x:frame_x+resized_sprite.shape[1], c] * (1.0 - resized_sprite[:, :, 3] / 255.0)

        # Write the modified frame to the output video
        out.write(frame)

        frame_num += 1
        if frame_num % 1 == 0: 
            SIZE = min(SIZE+SIZE_CHANGE, MAXSIZE)
            ANGLE = max(ANGLE-ANGLE_CHANGE, 0)

    # Release the resources
    cap.release()
    out.release()

    print("The 1950s effect has been applied, and the output video is saved at:", output_path)

def customAddWeighted(src1, alpha, src2, beta, gamma=0):
    # Check if the images have the same size
    if src1.shape != src2.shape:
        raise ValueError("Input images must have the same size.")

    # Perform alpha blending
    blended_image = np.clip(src1 * alpha[:, :, np.newaxis] + src2 * beta[:, :, np.newaxis] + gamma, 0, 255).astype(
        np.uint8)

    return blended_image

if __name__ == "__main__":
    animated_box("/home/pydashninja/templetes/video.mp4",
                       0, 10, "/home/pydashninja/templetes/video2.mp4")
    print("here")
