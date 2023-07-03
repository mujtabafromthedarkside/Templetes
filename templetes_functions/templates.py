import random
import os
import cv2
from effects import *
import shutil


def template1(image_path):

    # make a random number
    random_number = random.randint(0, 10000)
    random_number = random_number + random.randint(0, 10000)
    temp_output = f'temp/{random_number}.mp4'

    # image_path, duration, fps, output_path
    create_video_from_image(image_path, 5, 30, temp_output)

    temp_output2 = f'temp/{random_number + 1}.mp4'

    apply_blinking_effect(temp_output, 1, 5, temp_output2)

    temp_output3 = f'temp/{random_number + 2}.mp4'

    tv_filter(temp_output2, 1, 5, temp_output3)

    temp_output4 = f'temp/{random_number + 3}.mp4'

    create_red_box_animation(temp_output3, 1, 5, temp_output4)

    # remove f'{random_number}.mp4' from directory temp and move f'{random_number + 1}.mp4' to directory output
    os.remove(temp_output)
    os.remove(temp_output2)
    os.remove(temp_output3)
    shutil.move(temp_output4, 'output')

    # play a video
    cap = cv2.VideoCapture(f'output/{random_number + 3}.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey(int(1000/fps)) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # remove files from a directory output/*
    for filename in os.listdir('output'):
        file_path = os.path.join('output', filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def template2(image_path):

    # make a random number
    random_number = random.randint(0, 10000)
    random_number = random_number + random.randint(0, 10000)
    temp_output = f'temp/{random_number}.mp4'

    # image_path, duration, fps, output_path
    create_video_from_image(image_path, 10, 30, temp_output)

    temp_output2 = f'temp/{random_number + 1}.mp4'

    shake(temp_output, 1, 5, temp_output2, shake_intensity=15)

    # temp_output3 = f'temp/{random_number + 2}.mp4'

    # tv_filter(temp_output2, 1, 5, temp_output3)

    # temp_output4 = f'temp/{random_number + 3}.mp4'

    # create_red_box_animation(temp_output3, 1, 5, temp_output4)

    # remove f'{random_number}.mp4' from directory temp and move f'{random_number + 1}.mp4' to directory output
    # os.remove(temp_output)
    # os.remove(temp_output2)
    # os.remove(temp_output3)
    shutil.move(temp_output2, 'output')

    # play a video
    cap = cv2.VideoCapture(f'output/{random_number + 1}.mp4')
    fps = cap.get(cv2.CAP_PROP_FPS)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('frame', frame)
        if cv2.waitKey(int(1000/fps)) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # remove files from a directory output/*
    for filename in os.listdir('output'):
        file_path = os.path.join('output', filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
