import cv2
import os
import numpy as np

def falling_squares(video_path, start_time, output_path):
    cap = cv2.VideoCapture(video_path)

    # Get video properties
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Calculate start and end frame numbers
    start_frame = int(start_time * fps)
    # frames_required = 10*fps                                        # in reality, takes 5-6 seconds. But it doesn't matter if it's more.
    # if frame_count < start_frame + frames_required:
    #     print("The time is too short to apply the effect.")
    #     return

    # Create VideoWriter object to save the output video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps,
                          (frame_width, frame_height))

    velocity = 30
    height, width = frame_height, frame_width
    borderSize, borderColor = 5 , (255,255,255)

    widthDivider, heightDivider = 3,3
    blockSizeW, blockSizeH = width//widthDivider , height//heightDivider
    numberBlocks = widthDivider * heightDivider
    numberBlocksDone = 0
    
    frame_num = 0
    last_frame = np.zeros((frame_height, frame_width, 3), np.uint8)

    BackgroundBorderThickness = 2
    for initial_x1, initial_x2 in reversed(list(zip(range(0,width-blockSizeW+1, blockSizeW), range(blockSizeW-BackgroundBorderThickness, width, blockSizeW)))):
        for initial_y1, initial_y2 in reversed(list(zip(range(0,height-blockSizeH+1, blockSizeH), range(blockSizeH-BackgroundBorderThickness, height, blockSizeH)))):
            # if numberBlocksDone == numberBlocks - 1:
            #     initial_x2 += BackgroundBorderThickness
            x1,x2 = initial_x1,initial_x2
            y12,y22 = initial_y1,initial_y2
            print(x1,y12, x2,y22)
            y11,y21 = -(y22-y12), borderSize

            squareReached = False
            diffColorFrames = 5
            diffColorFramesIter = 0
            squareFinalOnce = True
            squareFinalFrames = 10
            squareFinalFramesIter = 0
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                # Copy the original img
                if (frame_num < start_frame):
                    # print("Not the right frames")
                    out.write(frame)
                    frame_num += 1
                    continue

                square = frame[initial_y1: initial_y2, initial_x1: initial_x2].copy()
                # square = 255 - square
                square = cv2.cvtColor(square, cv2.COLOR_BGR2GRAY)
                square = np.stack([square, square, square], axis=-1)
                # print(square.shape)

                frame = last_frame.copy()
                if y11 != y12 or y21 != y22:
                    y11 = min(y11+velocity, y12)
                    y21 = min(y21+velocity, y22)
                if y11 < 0:
                    # frame[0:y21, x1:x2] = square[0:y21, :]
                    frame[0:y21, x1:x2] = cv2.copyMakeBorder(square[0+borderSize:y21-borderSize, borderSize: -borderSize],borderSize,borderSize,borderSize,borderSize,cv2.BORDER_CONSTANT,value=borderColor)    
                elif (y11 == y12) and (y21 == y22):
                    squareReached = True
                    breakFlag = False
                    if diffColorFramesIter < diffColorFrames:
                        # print(1)
                        diffColorFramesIter += 1
                    elif squareFinalOnce:
                        # print(2)
                        # square = 255 - square
                        squareFinalOnce = False
                    elif squareFinalFramesIter < squareFinalFrames:
                        # print(3)
                        squareFinalFramesIter += 1
                    else:
                        # print(4)
                        breakFlag = True
                        numberBlocksDone += 1
                    frame[y11:y21, x1:x2] = square
                    if breakFlag:
                        print('breakFlag')
                        break
                else:
                    # print("complete invert")
                    frame[y11:y21, x1:x2] = cv2.copyMakeBorder(square[0+borderSize:y21-borderSize, borderSize: -borderSize],borderSize,borderSize,borderSize,borderSize,cv2.BORDER_CONSTANT,value=borderColor)
                # print(y11, y21, y12, y22)
                # cv2.imshow('Falling squares', frame)
                # if cv2.waitKey(int(1000/fps)) & 0xFF == ord('q'):
                #     break
                out.write(frame)
                frame_num += 1

                # Exit the loop if 'q' is pressed
                # if cv2.waitKey(30) & 0xFF == ord('q'):
                    # break
            # print('continuing')
            if not cap.isOpened():
                print('cap is not open')
            if frame is not None: last_frame = frame.copy()

    if numberBlocksDone != numberBlocks:
        print("The time is too short to apply the effect.")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        out.write(frame)
        frame_num += 1

    # Release the resources
    cap.release()
    out.release()

    print("The falling squares effect has been applied, and the output video is saved at:", output_path)
