import numpy as np
from pathlib import Path
import argparse
import cv2
import os
import csv

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("target_directory", help="The directory in which the image and .tif files are stored.")
    parser.add_argument("tif_files", nargs="+", help="The .tif files serving as background, midground, and foreground roi masks respectively.")
    parser.add_argument("--analyze", action="store_true", default=False, help="If given, only calculates focus values to determine thresholds for a given set of images.")
    parser.add_argument("--predict", action="store_true", default=False, help="If given, calculates focus values and predicts amount of fog present in a given set of images. --thresholds is required.")
    parser.add_argument("--thresholds", nargs="+", help="The threshold values distinguishing clear from light fog and light fog from heavy fog for the background, midground, and foreground of the image respectively.")

    args = parser.parse_args()

    image_dir = Path(args.target_directory)
    mask_background = cv2.imread(f"{args.target_directory}/{args.tif_files[0]}")
    mask_midground = cv2.imread(f"{args.target_directory}/{args.tif_files[1]}")
    mask_foreground = cv2.imread(f"{args.target_directory}/{args.tif_files[2]}")
    mask_list = [mask_background, mask_midground, mask_foreground]

    data_file = open(f"{args.target_directory}/Blur_Detection.csv", "w")
    data_file.write("Filename,Background Focus,Midground Focus,Foreground Focus,\n")

    # Loop through each image in the directory
    for photo in os.scandir(image_dir):
        if photo.is_file() and photo.name.endswith(".jpg"):
            image = cv2.imread(f"{args.target_directory}/{photo.name}")
            # Apply a Gaussian blur to the image to reduce noise and convert to gray scale
            smoothed_image = cv2.GaussianBlur(image, (5, 5), 0)
            gray_image = cv2.cvtColor(smoothed_image, cv2.COLOR_BGR2GRAY)
            # Calculate focus values for background, midground, and foreground
            fft_focus_values = calculate_focus(gray_image, mask_list)
            # Write to file
            data_file.write(f"{photo.name},{fft_focus_values[0]},{fft_focus_values[1]},{fft_focus_values[2]},\n")

    data_file.close()

def calculate_brightness(gray):
    """Computes the average brightness of an image using numpy mean.
    
    :param gray: A grayscale version of the image to be analyzed.
    :type gray: numpy array"""
    average_brightness = np.mean(gray)
    return average_brightness

def calculate_focus(image, masks):
    """Computes the amount of blur in an image using a Fast Fourier transform.
    
    :param image: The image to be analyzed, converted to grayscale with a Gaussian blur applied.
    :param masks: An array of roi masks to be applied to the image.
    :type image: numpy array
    :type masks: list"""

    # Apply a fourier fast transform to the image
    (height, width) = image.shape
    (centerX, centerY) = width // 2, height // 2
    fft_shift = np.fft.fftshift(np.fft.fft2(image))
    radius = 40
    fft_shift[centerY - radius:centerY + radius, centerX - radius:centerX + radius] = 0
    recon = np.fft.ifft2(np.fft.ifftshift(fft_shift))
    magnitude = 20 * np.log(np.abs(recon) + 1e-8)
    
    focus_values = []

    # Temporarily save the resulting image as a .jpg file in order to apply the roi masks
    cv2.imwrite("fft.jpg", magnitude)
    fft_image = cv2.imread(f"fft.jpg")

    # Apply each successive roi mask to obtain the focus value from each image segment
    for mask in masks:
        masked_image = cv2.bitwise_and(fft_image, mask)
        focus_values.append(float(np.mean(masked_image)))
    
    os.remove(Path("fft.jpg"))
    return focus_values

main()