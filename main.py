import cv2
import random
import os
import shutil
from effects import create_video_from_image, apply_blinking_effect, tv_filter
# read image


img = cv2.imread('1.jpg')
# get image shape

# make a random number
random_number = random.randint(0, 10000)
random_number = random_number + random.randint(0, 10000)
temp_output = f'temp/{random_number}.mp4'

# image_path, duration, fps, output_path
create_video_from_image('1.jpg', 10, 30, temp_output)

temp_output2 = f'temp/{random_number + 1}.mp4'

apply_blinking_effect(temp_output, 1, 4, temp_output2)

temp_output3 = f'temp/{random_number + 2}.mp4'

tv_filter(temp_output2, 5, 9, temp_output3)


# remove f'{random_number}.mp4' from directory temp and move f'{random_number + 1}.mp4' to directory output
os.remove(temp_output)
os.remove(temp_output2)
shutil.move(temp_output3, 'output')


# play a video
cap = cv2.VideoCapture(f'output/{random_number + 2}.mp4')
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
