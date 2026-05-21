import argparse
from io import BytesIO
import os
from pathlib import Path
import random
import requests
import json

from PIL import Image
import cv2 as cv

def main():
    parser = argparse.ArgumentParser(description="Classify images from a coast redwood PhenoCam site based on fog quantity")

    parser.add_argument("site_name", help="The site to draw images from")
    parser.add_argument("start_date", help="The earliest date to draw images from - format as YYYY/MM/DD")
    parser.add_argument("end_date", help="The latest date to draw images from - format as YYYY/MM/DD")
    parser.add_argument("download_directory", help="The filepath to the directory which images and results are saved to")
    parser.add_argument("num_photos", help="The total number of images to be downloaded")

    args = parser.parse_args()

    urls_received = get_image_urls(args.site_name, args.download_directory)

    if (urls_received):
        download(args.site_name, args.start_date, args.end_date, args.download_directory, args.num_photos)

        print("This is a program to classify images based on the level of fog they contain. Please rate images according to the following ranking system: ")
        print_instructions()

        classify(args.site_name, args.download_directory)

def print_instructions():
    print("0 - Dark (Only for images in which nothing is visible)")
    print("1 - Clear Day")
    print("2 - Light Fog in Background, Clear in Midground and Foreground")
    print("3 - Heavy Fog in Background, Clear in Midground and Foreground")
    print("4 - Heavy Fog in Background, Light Fog in Midground, Clear in Foreground")
    print("5 - Heavy Fog in Background and Midground, Clear in Foreground")
    print("6 - Heavy Fog in Background and Midground, Light Fog in Foreground")
    print("7 - Heavy Fog in Background, Midground, and Foreground")

def get_image_urls(site_name, save_to):
    """Saves urls for all phenocam images from a given site to a .txt file.
    
    :param site_name: The name of the site to obtain images from.
    :type site_name: str
    :param save_to: The filepath to the destinate directory for the image urls.
    :type save_to: str
    """

    # Check that the directory we are saving to exists
    if type(save_to) is not Path:
        save_dir = Path(save_to)
    else:
        save_dir = save_to
    if not save_dir.is_dir():
        os.mkdir(save_dir)

    output_filepath = Path(f"{save_to}/{site_name}_urls.txt")
    output_filename = f"{save_to}/{site_name}_urls.txt"

    # Check whether image urls have already been downloaded
    if not output_filepath.is_file():
        try: 
            response = requests.get(f"https://phenocam.nau.edu/api/siteimagelist/{site_name}")
            data = response.json()
            with open(output_filename, "w+") as url_file:
                for url in data["imagelist"]:
                    print(url, file=url_file)
            return True
        except:
            print("Error accessing given site - site name may be incorrect.")
            return False
    else:
        return True

def download(site_name, start_date, end_date, save_to, n_photos):
    """Downloads photos taken in some time range at a given site.

    :param site_name: The name of the site to download from.
    :type site_name: str
    :param start_date: The starting date to draw images from.
    :type start_date: str
    :param end_date: The ending date to draw images from.
    :type end_date: str
    :param save_to: The destination directory for downloaded images. If the
        directory already exists, it is NOT cleared. New photos are added to
        the directory, except for duplicates, which are skipped.
    :type save_to: str
    :param n_photos: The number of photos to download.
    :type n_photos: int
    """
    
    urls_filename = f"{save_to}/{site_name}_urls.txt"

    start_url = f"https://phenocam.nau.edu/webcam/browse/{site_name}/{start_date}"
    end_url = f"https://phenocam.nau.edu/webcam/browse/{site_name}/{end_date}"

    start_date_split = start_date.split("/")
    end_date_split = end_date.split("/")

    start_img_url = f"https://phenocam.nau.edu/data/archive/{site_name}/{start_date_split[0]}/{start_date_split[1]}/{site_name}_{start_date_split[0]}_{start_date_split[1]}_{start_date_split[2]}"
    end_img_url = f"https://phenocam.nau.edu/data/archive/{site_name}/{end_date_split[0]}/{end_date_split[1]}/{site_name}_{end_date_split[0]}_{end_date_split[1]}_{end_date_split[2]}"

    url_list = []

    # Check to make sure both dates are accessible within the site data
    try:
        resp1 = requests.get(start_url, timeout=10)
    except:
        print("Error accessing data - given start date is not accessible for this site.")

    try:
        resp2 = requests.get(end_url, timeout=10)
    except:
        print("Error accessing data - given end date is not accessible for this site.")

    if resp1.ok and resp2.ok:
        n_downloaded = 0
        # Add all urls for images that fall between the given dates to a list
        with open(urls_filename, "r") as urls_file:
            for line in urls_file:
                if start_img_url <= line.strip() <= end_img_url:
                    url_list.append(line.strip())
        # Randomly choose a set of image urls from that list and download each corresponding image
        while n_downloaded < int(n_photos):
            image_url = random.choice(url_list)
            try:
                image_response = requests.get(image_url, timeout=10)
            except Exception as e:
                print(f"ERROR:{e}")
            if image_response.ok:
                image_url_split = image_url.split("/")
                output_fpath = Path(f"{save_to}/{image_url_split[-1]}")
                # Check to make sure the image hasn't already been downloaded - if so, it gets skipped
                if not output_fpath.is_file():
                    try:
                        img = Image.open(BytesIO(image_response.content))
                        img.save(output_fpath)
                        n_downloaded += 1
                    except Exception as e:
                        print(f"ERROR:{e}")

def classify(site_name, save_to):
    """Allows user to classify images based on level of fogginess

    :param site_name: The name of the site to obtain images from.
    :type site_name: str
    :param save_to: The filepath to the destinate directory for the image urls.
    :type save_to: str
    """
    image_dir = Path(save_to)
    csv_filename = f"{save_to}/{site_name}_fogdata.csv"

    with open(csv_filename, "a") as csv_file:
        # Loop through files in the directory and check whether each is an image file
        index = 0
        for photo in image_dir.iterdir():
            if photo.is_file():
                extension = photo.name.split(".")[-1]
                if (extension == "jpg"):
                    image_location = f"{save_to}/{photo.name}"
                    img = cv.imread(image_location)
                    # Resize and move image so it can be displayed side by side with the terminal window
                    resized_image = cv.resize(img, (648, 480))
                    cv.imshow(photo.name, resized_image)
                    cv.moveWindow(photo.name, 880, 310)
                    cv.waitKey(1)
                    # Collect user input for level of fogginess and record in .csv file
                    user_input = input("Enter level of fogginess: ")
                    while (user_input < "0" or user_input > "7"):
                        user_input = input("Please enter a number between 0 and 7: ")
                    csv_file.write(f"{photo.name},{user_input}\n")
                    cv.destroyAllWindows()
                    cv.waitKey(1) 
                    if (index % 40 == 0):
                        print_instructions()

main()