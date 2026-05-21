import argparse
from datetime import datetime
from io import BytesIO
import os
from pathlib import Path
import random
import requests
import json

import numpy as np
import pandas as pd
from PIL import Image

def main():
    parser = argparse.ArgumentParser(description="Classify images from a coast redwood PhenoCam site based on fog quantity")

    parser.add_argument("site_name", help="The site to draw images from")
    parser.add_argument("start_date", help="The earliest date to draw images from - format as YYYY/MM/DD")
    parser.add_argument("end_date", help="The latest date to draw images from - format as YYYY/MM/DD")
    parser.add_argument("download_directory", help="The filepath to the directory which images and results are saved to")

    args = parser.parse_args()

    urls_received = get_image_urls(args.site_name, args.download_directory)

    if (urls_received):
        download(args.site_name, args.start_date, args.end_date, args.download_directory, 3)

        #classify(args.download_directory)

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
    :param dates: A 2-tuple indicating the oldest and youngest allowable
        photos.
    :type dates: Tuple[str, str]
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
        with open(urls_filename, "r") as urls_file:
            for line in urls_file:
                if start_img_url <= line.strip() <= end_img_url:
                    url_list.append(line.strip())

        while n_downloaded < n_photos:
            image_url = random.choice(url_list)
            try:
                image_response = requests.get(image_url, timeout=10)
            except Exception as e:
                print(f"ERROR:{e}")
            if image_response.ok:
                image_url_split = image_url.split("/")
                output_fpath = Path(f"{save_to}/{image_url_split[-1]}")
                if not output_fpath.is_file():
                    try:
                        img = Image.open(BytesIO(image_response.content))
                        img.save(output_fpath)
                        n_downloaded += 1
                    except Exception as e:
                        print(f"ERROR:{e}")

def classify(save_to):
    """Allows user to classify images based on level of fogginess
    """
    image_dir = Path(save_to)

    for photo in image_dir.iterdir():
        if photo.is_file():
            extension = photo.name.split(".")[-1]
            if (extension == "jpg"):
                image_location = f"{save_to}/{photo.name}"
                img = Image.open(image_location)
                img.show()  
                user_input = input("Enter level of fogginess: ")
                img.close()

main()