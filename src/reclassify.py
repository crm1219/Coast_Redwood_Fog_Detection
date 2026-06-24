import os
import cv2 as cv
import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("site_name", help="The site to draw images from")

    args = parser.parse_args()

    reclassify(args.site_name)

def reclassify(site_name):
    csv_file1 = open(f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/{site_name}/{site_name}_fogdata.csv", "r")
    csv_file2 = open(f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/{site_name}test/{site_name}_fogdata.csv", "r")
    new_file1 = open(f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/{site_name}/{site_name}_fogdata1.csv", "w")
    new_file2 = open(f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/{site_name}test/{site_name}_fogdata1.csv", "w")

    for line in csv_file1:
        photo_name = line.split(",")[0]
        image_location = f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/{site_name}/{photo_name}"
        img = cv.imread(image_location)

        # Resize and move image so it can be displayed side by side with the terminal window
        resized_image = cv.resize(img, (778, 576))
        cv.imshow(photo_name, resized_image)
        cv.moveWindow(photo_name, 700, 250)
        cv.waitKey(1)

        # Collect user input for level of fogginess and record in .csv file
        user_input = input("Enter level of fogginess: ")
        while (user_input < "0" or user_input > "8"):
            user_input = input("Please enter a number between 0 and 8: ")
        new_file1.write(f"{photo_name},{user_input}\n")
        cv.destroyAllWindows()
        cv.waitKey(1) 

    for line in csv_file2:
        photo_name = line.split(",")[0]
        image_location = f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/{site_name}test/{photo_name}"
        img = cv.imread(image_location)

        # Resize and move image so it can be displayed side by side with the terminal window
        resized_image = cv.resize(img, (778, 576))
        cv.imshow(photo_name, resized_image)
        cv.moveWindow(photo_name, 700, 250)
        cv.waitKey(1)

        # Collect user input for level of fogginess and record in .csv file
        user_input = input("Enter level of fogginess: ")
        while (user_input < "0" or user_input > "8"):
            user_input = input("Please enter a number between 0 and 8: ")
        new_file2.write(f"{photo_name},{user_input}\n")
        cv.destroyAllWindows()
        cv.waitKey(1) 

    csv_file1.close()
    csv_file2.close()
    new_file1.close()
    new_file2.close()

main()