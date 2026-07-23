import numpy as np
from pathlib import Path
import argparse
import cv2
import os
import csv
import sys

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("target_directory", help="The directory in which the files are stored")
    parser.add_argument("--sky_tif_file", help="The tif file to be used as an roi mask for the sky")
    parser.add_argument("--tree_tif_files", nargs="+", help="The tif files to be used as roi masks for regions with trees")

    args = parser.parse_args()

    image_dir = Path(args.target_directory)
    mask_background = cv2.imread(f"{args.target_directory}/{args.background_tif_file}")
    mask_midground = cv2.imread(f"{args.target_directory}/{args.midground_tif_file}")
    mask_foreground = cv2.imread(f"{args.target_directory}/{args.foreground_tif_file}")
    mask_list = [mask_background, mask_midground, mask_foreground]

    data_file_path = f"{args.target_directory}/Blur_Detection.csv"
    data_file = open(f"{args.target_directory}/Blur_Detection.csv", "r")
    #data_file.write("Filename,Background Focus,Background Fog,Midground Focus,Midground Fog,Foreground Focus,Foreground Fog\n")

    image_data = open(f"{args.target_directory}/Image_Data1.csv", "r")

    index = 0
    totals = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    counts = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    averages = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    #for photo in os.scandir(image_dir):
    #    if photo.is_file() and photo.name.endswith(".jpg"):
    main_index = 0
    for line in image_data:
        if main_index != 0:
            photo = line.split(",")[0]
            total_rating = line.split(",")[4]
            if int(total_rating) != 7 and int(total_rating) != 8:
                image = cv2.imread(f"{args.target_directory}/{photo}")
                ratings = [int(line.split(",")[1]), int(line.split(",")[2]), int(line.split(",")[3])]
                index = 0
                focus_values = [0, 0, 0]
                for mask in args.tif_files:
                    mask_path = cv2.imread(f"{args.target_directory}/{mask}")
                    masked_image = cv2.bitwise_or(image, mask_path)
                    gray_image = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
                    brightness = compute_brightness(gray_image)
                    focus_values[index] = brightness
                    totals[index][ratings[index]] += brightness
                    counts[index][ratings[index]] += 1
                    index += 1
                data_file.write(f"{photo},{focus_values[0]},{focus_values[1]},{focus_values[2]},\n")
        main_index += 1

    data_file.close()
    image_data.close()

    for i in range(3):
        if i == 0:
            print("Background fog averages:")
        elif i == 1:
            print("Midground fog averages:")
        elif i == 2:
            print("Foreground fog averages:")
        for j in range(3):
            if j == 0:
                print(f"Clear average: {totals[i][j] / counts[i][j]}")
            elif j == 1:
                print(f"Light average: {totals[i][j] / counts[i][j]}")
            elif j == 2:
                print(f"Heavy average: {totals[i][j] / counts[i][j]}")

def compute_brightness(gray):
    """Computes the average brightness of an image using numpy mean.
    
    :param gray: A grayscale version of the image to be analyzed.
    :type gray: numpy array"""
    average_brightness = np.mean(gray)
    return average_brightness

def get_roi_stats(im, roimask):
    """
    Function to return a collection of stats for DN values for an image / mask pair.
    """
 
    # split into bands
    (im_r, im_g, im_b) = im.split()

    # create numpy arrays with bands
    r_array = np.asarray(im_r, dtype=np.int16)
    g_array = np.asarray(im_g, dtype=np.int16)
    b_array = np.asarray(im_b, dtype=np.int16)

    # try applying mask to red image ... if mask and image don't
    # have same size this will raise an exception.
    try:
        r_ma = np.ma.array(r_array,mask=roimask)
    except:
        errstr = "Error applying mask to image file.\n"
        sys.stderr.write(errstr)
        return None

    # make masked arrays for G,B
    g_ma = np.ma.array(g_array,mask=roimask)
    b_ma = np.ma.array(b_array,mask=roimask)

    # find mean, std
    r_vals = r_ma.compressed()
    r_mean = r_vals.mean()

    g_vals = g_ma.compressed()
    g_mean = g_vals.mean()

    b_vals = b_ma.compressed()
    b_mean = b_vals.mean()
    
    return  g_mean / r_mean

main()