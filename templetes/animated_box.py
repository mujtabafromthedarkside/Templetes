import cv2
import os
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
    sprite = cv2.imread(os.path.join('templetes', 'assets','subscribe2.png'), cv2.IMREAD_UNCHANGED)
    sprite2 = cv2.imread(os.path.join('templetes', 'assets','youtube.png'), cv2.IMREAD_UNCHANGED)
    sprite = changeColor(sprite, [0,0,255,255],[255,255,255,255], [255,255,255])
    
    # Loop through the frames and apply the effect
    frame_num = 0
    MAXSIZE = 100
    FINAL_STATE_REACHED_ONCE = False
    FINAL_STATE_REACHED = False

    SIZE = 0
    ANGLE = 90

    SIZE_CHANGE = 4
    ANGLE_CHANGE = 2

    MAX_SPRITE2_TRANSLATION = MAXSIZE + MAXSIZE // 4
    SPRITE2_TRANSLATION = 0
    SPRITE2_TRANSLATION_CHANGE = 4
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Apply the effect only within the specified interval
        if start_frame <= frame_num <= end_frame:
            # Calculate the position to place the second image in the middle of the first image
            if FINAL_STATE_REACHED_ONCE: 
                sprite = changeColor(sprite, [255,255,255,255],[0,0,0,255], [255,255,255])
                FINAL_STATE_REACHED = True

            resized_sprite = cv2.resize(sprite, (SIZE,SIZE))

            if FINAL_STATE_REACHED:
                resized_sprite2 = cv2.resize(sprite2, (SIZE,SIZE))
                SPRITE2_TRANSLATION = min(SPRITE2_TRANSLATION + SPRITE2_TRANSLATION_CHANGE, MAX_SPRITE2_TRANSLATION)
                
                if SPRITE2_TRANSLATION == MAX_SPRITE2_TRANSLATION and SPRITE2_TRANSLATION - SPRITE2_TRANSLATION_CHANGE != MAX_SPRITE2_TRANSLATION:
                    resized_sprite2 = changeColor(resized_sprite2, [255,255,255,255],[0,0,0,255], [255,255,255])
                for c in range(0, 3):
                    frame[frame_y-SPRITE2_TRANSLATION:frame_y+resized_sprite2.shape[0]-SPRITE2_TRANSLATION, frame_x:frame_x+resized_sprite2.shape[1], c] = resized_sprite2[:, :, c] * (resized_sprite2[:, :, 3] / 255.0) + frame[frame_y-SPRITE2_TRANSLATION:frame_y+resized_sprite2.shape[0]-SPRITE2_TRANSLATION, frame_x:frame_x+resized_sprite2.shape[1], c] * (1.0 - resized_sprite2[:, :, 3] / 255.0)


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
            MAXSIZE_REACHED_ONCE = (SIZE != MAXSIZE)
            MAXANGLE_REACHED_ONCE = (ANGLE != 0)

            SIZE = min(SIZE+SIZE_CHANGE, MAXSIZE)
            ANGLE = max(ANGLE-ANGLE_CHANGE, 0)

            MAXSIZE_REACHED_ONCE = (SIZE == MAXSIZE) and MAXSIZE_REACHED_ONCE
            MAXANGLE_REACHED_ONCE = (ANGLE == 0) and MAXANGLE_REACHED_ONCE

            FINAL_STATE_REACHED_ONCE = MAXSIZE_REACHED_ONCE and (0 == ANGLE)
            FINAL_STATE_REACHED_ONCE = (MAXANGLE_REACHED_ONCE and (MAXSIZE == SIZE)) or FINAL_STATE_REACHED_ONCE
            
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

def changeColor(imgArray, replacement_color_shape, replacement_color_text, target_color_text):
    # target_color_shape = np.array([0,0,0])
    # target_color_shape2 = np.array([1,1,1])
    # target_color_text = np.array([255,255,255])
    target_color_text = np.array(target_color_text)

    replacement_color_shape = np.array(replacement_color_shape)
    replacement_color_text = np.array(replacement_color_text)
    for i in range(len(imgArray)):
        for j in range(len(imgArray[i])):
            # pixel shouldn't be transparent.
            if imgArray[i][j][3] == 0:
                continue

            pixel_shape = True
            pixel_text = True

            for k in range(3):
                # if imgArray[i][j][k] != target_color_shape[k] and imgArray[i][j][k] != target_color_shape2[k]:
                #     pixel_shape = False
                if imgArray[i][j][k] != target_color_text[k]:
                    pixel_text = False

            # if it indeed is shape, change to new shape color
            if not pixel_text:
                imgArray[i][j] = replacement_color_shape
            # if it indeed is text, change to new text color
            else:
                imgArray[i][j] = replacement_color_text

            # if pixel_shape or pixel_text or imgArray[i][j][3] == 0:
            #     continue
            # print(imgArray[i][j])

    # Create a mask for the pixels that match the target color
    # mask1 = np.all((imgArray[...,:3] == target_color), axis=-1)
    # print(mask1.shape)
    # print(imgArray[..., 3].shape)
    # mask2 = np.all((imgArray[...,3] == [0]), axis=-1)
    # print(mask2.shape)

    # # Apply the replacement color to the pixels that match the target color
    # imgArray[mask1] = replacement_color
    return imgArray

if __name__ == "__main__":
    animated_box("/home/pydashninja/templetes/video.mp4",
                       0, 10, "/home/pydashninja/templetes/video2.mp4")
    print("here")
