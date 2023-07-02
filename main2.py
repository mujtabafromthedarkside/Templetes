import cv2
import random
import os
import shutil
from effects import create_video_from_image, apply_blinking_effect, tv_filter
from templetes import animated_box
# read image

imgName = '1.jpeg'
img = cv2.imread(imgName)

# get image shape
print(img.shape)

# make a random number
random_number = random.randint(0, 10000)
random_number = random_number + random.randint(0, 10000)
temp_outputs = [f'temp/{random_number}.mp4']

# image_path, duration, fps, output_path
if not os.path.exists('temp'):
    os.mkdir('temp')
create_video_from_image(imgName, 5, 30, temp_outputs[-1])

random_number += 1
temp_outputs.append(f'temp/{random_number}.mp4')
tv_filter(temp_outputs[-2], 4,5, temp_outputs[-1])

random_number += 1
temp_outputs.append(f'temp/{random_number}.mp4')
animated_box(temp_outputs[-2], 1,5, temp_outputs[-1])

# # remove f'{random_number}.mp4' from directory temp and move f'{random_number + 1}.mp4' to directory output
for i in range(0,len(temp_outputs)-1):
    os.remove(temp_outputs[i])
if not os.path.exists('output'):
    os.mkdir('output')
shutil.move(temp_outputs[-1], 'output')

# play a video
cap = cv2.VideoCapture(f'output/{os.path.basename(temp_outputs[-1])}')
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
