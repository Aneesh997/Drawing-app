import cv2
import os

def convert_to_grayscale(input_path, output_folder, filename):
    # Read image
    img = cv2.imread(os.path.abspath(input_path))

    if img is None:
        raise ValueError("Image not loaded properly")

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Create new filename
    gray_name = f"gray_{filename}"
    gray_path = os.path.join(output_folder, gray_name)

    # Save grayscale image
    cv2.imwrite(gray_path, gray)

    return gray_path