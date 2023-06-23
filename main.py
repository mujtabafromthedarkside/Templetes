import cv2
import random
import os
import shutil
from effects import create_video_from_image, apply_blinking_effect
# read image

imgName = '1.jpeg'
img = cv2.imread(imgName)
# get image shape

# make a random number
random_number = random.randint(0, 10000)
random_number = random_number + random.randint(0, 10000)
temp_output = f'temp/{random_number}.mp4'

# image_path, duration, fps, output_path
if not os.path.exists('temp'):
    os.makedirs('temp')
create_video_from_image(imgName, 3, 10, temp_output)

temp_output2 = f'temp/{random_number + 1}.mp4'

apply_blinking_effect(temp_output, 2, 2, temp_output2)

# remove f'{random_number}.mp4' from directory temp and move f'{random_number + 1}.mp4' to directory output
os.remove(temp_output)
shutil.move(temp_output2, 'output')
