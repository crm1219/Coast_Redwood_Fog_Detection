# Allows the user to download a selection of random images, each of which they can evaluate to determine whether they want to keep or not, and classify each image

import argparse
from io import BytesIO
from pathlib import Path
import random
import requests
import os

from PIL import Image
import cv2 as cv

def main():
    parser = argparse.ArgumentParser(description="Classify images from a coast redwood PhenoCam site based on fog quantity")

    parser.add_argument("site_name", help="The site to draw images from")
    parser.add_argument("start_date", help="The earliest date to draw images from - format as YYYY/MM/DD")
    parser.add_argument("end_date", help="The latest date to draw images from - format as YYYY/MM/DD")
    parser.add_argument("download_directory", help="The filepath to the directory which images and results are saved to")
    parser.add_argument("--exclude_directory", default="", help="The filepath to a directory containing images to exclude.")
    parser.add_argument("num_photos", help="The total number of images to be downloaded")

    args = parser.parse_args()

    # Check that the given directory exists
    save_to = args.download_directory
    save_dir = Path(args.download_directory)
    while not save_dir.exists():
        save_to = input("Given filepath is invalid - please input a valid path to the download directory: ")
        save_dir = Path(save_to)

    exclude = args.exclude_directory
    if exclude != "":
        exclude_dir = Path(exclude)
        while not exclude_dir.exists():
            exclude = input("Given filepath is invalid - please input a valid path to the exclusion directory: ")
            exclude_dir = Path(exclude)

    # Check that number of photos provided is valid
    num_photos = args.num_photos
    while int(num_photos) <= 0:
        num_photos = input("Number of photos to download must be positive - please input a valid number: ")

    # Download urls for all site images
    urls_received = get_image_urls(args.site_name, save_to)

    # If successful, download a random selection of images from the given date range
    if urls_received:
        chosen_images = download(args.site_name, args.start_date, args.end_date, save_to, exclude, num_photos)

        # If successful, allow user to classify images
        if chosen_images:
            print("\n\nThis is a program to classify images based on the level of fog they contain. Please rate images according to the following ranking system: ")
            print_instructions()

            classify(args.site_name, save_to, chosen_images)

def print_instructions():
    """Prints instructions for rating images."""
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

    # Check to see if given site exists
    site_url = f"https://phenocam.nau.edu/webcam/browse/{site_name}"
    try: 
        response = requests.get(site_url)
    except:
        print("ERROR: Given site cannot be accessed - site name may be incorrect.")
        return False
    if response.status_code == 404:
        print("ERROR: Given site cannot be accessed - site name may be incorrect.")
        return False
    
    # Designate .txt file to store urls
    output_filepath = Path(f"{save_to}/{site_name}_urls.txt")
    output_filename = f"{save_to}/{site_name}_urls.txt"

    # Check whether image urls have already been downloaded
    if not output_filepath.is_file():
        try: 
            list_response = requests.get(f"https://phenocam.nau.edu/api/siteimagelist/{site_name}")
        except Exception as e:
            print(f"ERROR: {e}\n")
            return False
        
        # Copy image urls into the .txt file
        image_list = list_response.json()
        with open(output_filename, "w+") as url_file:
            for url in image_list["imagelist"]:
                print(url, file=url_file)
    
    return True

def download(site_name, start_date, end_date, save_to, exclude, n_photos):
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
    :param exclude: A directory already containing images from the given site, meant to be excluded so images are not duplicated.
    :type exclude: str
    :param n_photos: The number of photos to download.
    :type n_photos: int
    """
    
    urls_filename = f"{save_to}/{site_name}_urls.txt"

    url_list = []
    chosen_images = []

    # Check if either date is incorrectly formatted
    start_date_split = start_date.split("/")
    end_date_split = end_date.split("/")
    
    if (len(start_date_split) != 3):
        print("ERROR: Given start date is incorrectly formatted.")
        return chosen_images
    if (len(end_date_split) != 3):
        print("ERROR: Given end date is incorrectly formatted.")
        return chosen_images

    start_img_url = f"https://phenocam.nau.edu/data/archive/{site_name}/{start_date_split[0]}/{start_date_split[1]}/{site_name}_{start_date_split[0]}_{start_date_split[1]}_{start_date_split[2]}"
    end_img_url = f"https://phenocam.nau.edu/data/archive/{site_name}/{end_date_split[0]}/{end_date_split[1]}/{site_name}_{end_date_split[0]}_{end_date_split[1]}_{end_date_split[2]}"

    n_downloaded = 0
    
    # Add all urls for images that fall between the given dates to a list
    with open(urls_filename, "r") as urls_file:
        for line in urls_file:
            if start_img_url <= line.strip() <= end_img_url:
                url_list.append(line.strip())
    
    # Check if the list is not empty
    if (url_list):
        # Randomly choose a set of image urls from that list and download each corresponding image
        while n_downloaded < int(n_photos):
            image_url = random.choice(url_list)
            try:
                image_response = requests.get(image_url, timeout=10)
            except Exception as e:
                print(f"ERROR: {e}\n")
            if image_response.ok:
                image_url_split = image_url.split("/")
                output_fpath = Path(f"{save_to}/{image_url_split[-1]}")
                exclude_fpath = Path(exclude)
                # Check to make sure the image hasn't already been downloaded - if so, it gets skipped
                if not output_fpath.is_file() and not exclude_fpath.is_file():
                    try:
                        photo = image_url_split[-1]
                        img = Image.open(BytesIO(image_response.content))
                        img.save(output_fpath)
                        new_img = cv.imread(output_fpath)

                        # Resize and move image so it can be displayed side by side with the terminal window
                        resized_image = cv.resize(new_img, (648, 480))
                        cv.imshow(photo, resized_image)
                        cv.moveWindow(photo, 880, 310)
                        cv.waitKey(1)

                        # Determine whether the user wants to keep or discard the photo
                        user_input = input("Enter 0 to discard and 1 to keep: ")
                        while (user_input < "0" or user_input > "1"):
                            user_input = input("Please enter a number between 0 and 1: ")
                        cv.destroyAllWindows()
                        cv.waitKey(1) 
                        if user_input == "0":
                            os.remove(output_fpath)
                        elif user_input == "1":
                            n_downloaded += 1
                            chosen_images.append(image_url_split[-1])
                            
                    except Exception as e:
                        print(f"ERROR: {e}\n")
    else:
        print("ERROR: No images are available for this site within the given date range.")
        
    return chosen_images

def classify(site_name, save_to, chosen_images):
    """Allows user to classify images based on level of fogginess

    :param site_name: The name of the site to obtain images from.
    :type site_name: str
    :param save_to: The filepath to the destinate directory for the image urls.
    :type save_to: str
    :param chosen_images: A list of filenames for each downloaded image.
    :type chosen_images: List(str)
    """

    csv_filename = f"{save_to}/{site_name}_fogdata.csv"

    with open(csv_filename, "a") as csv_file:
        index = 1
        for photo in chosen_images:
            image_location = f"{save_to}/{photo}"
            img = cv.imread(image_location)

            # Resize and move image so it can be displayed side by side with the terminal window
            resized_image = cv.resize(img, (648, 480))
            cv.imshow(photo, resized_image)
            cv.moveWindow(photo, 880, 310)
            cv.waitKey(1)

            # Collect user input for level of fogginess and record in .csv file
            user_input = input("Enter level of fogginess: ")
            while (user_input < "0" or user_input > "7"):
                user_input = input("Please enter a number between 0 and 7: ")
            csv_file.write(f"{photo},{user_input}\n")
            cv.destroyAllWindows()
            cv.waitKey(1) 

            # Reprint instructions at intervals
            if (index % 40 == 0):
                print_instructions()
            index += 1

main()