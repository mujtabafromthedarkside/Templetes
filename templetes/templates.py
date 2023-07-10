import random
import os
import cv2
from effects import *
import shutil
from utils import *

if not os.path.exists('output'):
    os.mkdir('output')
if not os.path.exists('temp'):
    os.mkdir('temp')

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


def template2(image_path, list_of_images):

    # make a random number
    random_number = random.randint(0, 10000)
    random_number = random_number + random.randint(0, 10000)
    temp_output = f'temp/{random_number}.mp4'

    # image_path, duration, fps, output_path
    create_video_from_image(image_path, 20, 30, temp_output)

    temp_output2 = f'temp/{random_number + 1}.mp4'

    shake(temp_output, 1, 6, temp_output2)

    temp_output3 = f'temp/{random_number + 2}.mp4'

    translate_in_circle(temp_output2, 7, 10, temp_output3)

    temp_output4 = f'temp/{random_number + 3}.mp4'

    switch_images_with_vibration(
        temp_output3, 11, 20, temp_output4, list_of_images)

    # remove f'{random_number}.mp4' from directory temp and move f'{random_number + 1}.mp4' to directory output
    temp_output5 = f'temp/{random_number + 4}.mp4'

    add_audio_to_video(temp_output4, "./audio/1.mp3", temp_output5)

    os.remove(temp_output)
    os.remove(temp_output2)
    os.remove(temp_output3)
    os.remove(temp_output4)
    shutil.move(temp_output5, 'output')
    print("Video with audio added successfully.")


# incomplete
def templete3(image_path):

    random_number = random.randint(0, 10000)
    random_number = random_number + random.randint(0, 10000)
    temp_output = f'temp/{random_number}.mp4'

    create_video_from_image(image_path, 10, 30, temp_output)

    temp_output2 = f'temp/{random_number + 1}.mp4'

    grey_image_in_window_vibrate_and_shifts(temp_output, 1, 10, temp_output2)

    os.remove(temp_output)
    shutil.move(temp_output2, 'output')
    print("Video with audio added successfully.")

    cap = cv2.VideoCapture(f'output/{random_number+1}.mp4')
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


def templete6(images_path_list):
    if len(images_path_list) > 2:
        print("Please provide only 2 images.")
        return
    random_number = random.randint(0, 10000)
    random_number = random_number + random.randint(0, 10000)
    temp_output = f'temp/{random_number}.mp4'

    create_video_from_image(images_path_list[0], 10, 30, temp_output)

    temp_output2 = f'temp/{random_number + 1}.mp4'

    YourAreNotCoolTemplate(
        images_path_list[1], temp_output, 1, 10, temp_output2)

    os.remove(temp_output)
    shutil.move(temp_output, 'output')

    cap = cv2.VideoCapture(f'output/{random_number+1}.mp4')
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

def templete4(image_path):
    random_number = random.randint(0, 10000)
    random_number = random_number + random.randint(0, 10000)
    temp_outputs = [os.path.join('temp',f'{random_number}.mp4')]

    create_video_from_image(image_path, 12, 30, temp_outputs[-1])

    random_number += 1
    temp_outputs.append(os.path.join('temp',f'{random_number}.mp4'))
    falling_squares(temp_outputs[-2], 0, temp_outputs[-1])

    # remove file if it already exists in output folder
    output_path = os.path.join('output', temp_outputs[-1][5:])
    print(f'saving final output to {output_path}')
    if os.path.exists(output_path):
        os.remove(output_path)

    shutil.move(temp_outputs[-1], 'output')

    # play a video
    cap = cv2.VideoCapture(f'output/{os.path.basename(temp_outputs[-1])}')
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f'{fps} fps')

    while cap.isOpened():
        wait_time = int(1000/fps/2)

        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('frame', frame)

        # pause on pressing spacebar
        if cv2.waitKey(wait_time) == ord(' '):
            print('paused video')
            wait_time = 0
        if wait_time == 0 and cv2.waitKey(wait_time):
            print("play video")
        elif cv2.waitKey(wait_time) == ord('q'):
            print('exit')
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

def templete5(image_path):
    random_number = random.randint(0, 10000)
    random_number = random_number + random.randint(0, 10000)
    temp_outputs = [os.path.join('temp',f'{random_number}.mp4')]

    create_video_from_image(image_path, 5, 30, temp_outputs[-1])

    random_number += 1
    temp_outputs.append(os.path.join('temp',f'{random_number}.mp4'))
    animated_box(temp_outputs[-2], 1,4, temp_outputs[-1])

    random_number += 1
    temp_outputs.append(os.path.join('temp',f'{random_number}.mp4'))
    tv_filter(temp_outputs[-2], 4,5, temp_outputs[-1])

    # remove file if it already exists in output folder
    output_path = os.path.join('output', temp_outputs[-1][5:])
    print(f'saving final output to {output_path}')
    if os.path.exists(output_path):
        os.remove(output_path)

    shutil.move(temp_outputs[-1], 'output')

    # play a video
    cap = cv2.VideoCapture(f'output/{os.path.basename(temp_outputs[-1])}')
    fps = cap.get(cv2.CAP_PROP_FPS)
    print(f'{fps} fps')

    while cap.isOpened():
        wait_time = int(1000/fps/2)

        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('frame', frame)

        # pause on pressing spacebar
        if cv2.waitKey(wait_time) == ord(' '):
            print('paused video')
            wait_time = 0
        if wait_time == 0 and cv2.waitKey(wait_time):
            print("play video")
        elif cv2.waitKey(wait_time) == ord('q'):
            print('exit')
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