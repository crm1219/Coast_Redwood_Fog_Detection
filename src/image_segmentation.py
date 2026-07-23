from PIL import Image
import numpy as np
import sys
from pathlib import Path
import argparse
import cv2

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("target_directory", help="The directory in which the files are stored")
    #parser.add_argument("site_name", help="The PhenoCam site from which the data comes")
    #parser.add_argument("tif_file", help="The name of the .tif file serving as the roi mask")

    args = parser.parse_args()

    image_dir = Path(args.target_directory)

    #mask_path = Path(f"{args.target_directory}/{args.tif_file}")
    #mask_img = Image.open(mask_path)
    #roimask = np.asarray(mask_img, dtype=np.bool)
    #new_roimask = cv2.imread(mask_path)


    index = 0
    totals = [0, 0, 0, 0, 0, 0, 0, 0]
    counts = [0, 0, 0, 0, 0, 0, 0, 0]
    averages = [0, 0, 0, 0, 0, 0, 0, 0]

    with open(f"{image_dir}/Image_Data1.csv") as data_file:
        for line in data_file:
            if index > 0:
                data = line.split(",")
                im_path = f"{image_dir}/{data[0]}"
                #im = Image.open(im_path)
                #im.load()
                #output = get_roi_stats(im, roimask)
                #print(f"Band analysis value for image {data[0]}: {output}\n")
                #im = cv2.imread(im_path)
                #gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                #output = compute_blur_brenner(gray)
                ##rating = int(data[1])
                #totals[rating] += output
                #counts[rating] += 1
                new_im = cv2.imread(im_path)
                #get_image_sharpness(new_im, new_roimask)
                edge_detection_test(args.target_directory, new_im, data[0])
            index += 1

    for i in range(8):
        if counts[i] != 0:
            averages[i] = totals[i] / counts[i]
        print(f"Average blur for rating {i}: {averages[i]}")

    data_file.close()


def get_image_sharpness(im, roimask):
    masked_image = cv2.bitwise_or(im, roimask)
    #gray = cv2.cvtColor(masked_image, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Combined Image", masked_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def edge_detection_test(directory, im, image_name):
    gaussian = cv2.GaussianBlur(im, (3, 3), 0)
    gray = cv2.cvtColor(gaussian, cv2.COLOR_BGR2GRAY)
    #sx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    #sy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    #gradient_magnitude = cv2.magnitude(sx, sy)
    # Convert to uint8
    #gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude)
    # Display result
    #cv2.imwrite(f"{directory}/{image_name.split(".")[0]}_sobel.jpg", gradient_magnitude)
    edges = cv2.Canny(gray, 75, 125)
    cv2.imwrite(f"{directory}/{image_name.split(".")[0]}_canny.jpg", edges)
    

main()