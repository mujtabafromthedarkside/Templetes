import cv2
import numpy as np


def zoom_and_translate(image_path, output_path, zoom_factor=1.5, pan_intensity=50):
    # Read the input image
    image = cv2.imread(image_path)

    # Get image dimensions
    image_height, image_width = image.shape[:2]

    # Zoom-in effect: Resize the image to larger dimensions
    new_width = int(image_width * zoom_factor)
    new_height = int(image_height * zoom_factor)
    zoomed_image = cv2.resize(image, (new_width, new_height))

    # Random translation (pan) effect
    dx, dy = np.random.randint(-pan_intensity, pan_intensity, size=2)
    translation_matrix = np.float32([[1, 0, dx], [0, 1, dy]])
    translated_image = cv2.warpAffine(
        zoomed_image, translation_matrix, (new_width, new_height))

    # Crop the result to the original size (to remove black borders)
    start_x, start_y = max(0, dx), max(0, dy)
    end_x, end_y = min(new_width, image_width +
                       dx), min(new_height, image_height + dy)
    cropped_image = translated_image[start_y:start_y +
                                     image_height, start_x:start_x+image_width]

    # Save the resulting image
    cv2.imwrite(output_path, cropped_image)

    print("Zoom and translation applied successfully.")


# Example usage
input_image_path = '1.jpg'
output_image_path = 'output_image_zoom_and_translation.jpg'
zoom_factor = 1.2  # 1.0 means no zoom, >1.0 means zoom-in
pan_intensity = 50  # The maximum number of pixels to pan in any direction
zoom_and_translate(input_image_path, output_image_path,
                   zoom_factor, pan_intensity)
