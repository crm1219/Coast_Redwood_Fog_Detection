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
        download(args.site_name, args.start_date, args.end_date, args.download_directory, 0)

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
    if type(save_to) is not Path:
        save_dir = Path(save_to)
    else:
        save_dir = save_to
    
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

    """

        while n_downloaded < n_photos:
            image_url = random.choice(url_list)
            try:
                image_response = requests.get(image_url, timeout=10)
            except Exception as e:
                print(f"ERROR:{e}")
            if image_response.ok:
                if output_fpath.is_file():
                    log_file.write(
                    f"WARN:{img_fname} was already downloaded, skipping\n")
                    break
                try:
                    img = Image.open(BytesIO(resp2.content))
                    img.save(output_fpath)
                    n_downloaded += 1
                    log_file.write(f"INFO:Retrieved {resp2.url}\n")
                except:
                    log_file.write(f"WARN:Could not read or save image from {resp2.url}\n")
    
"""
    """
    # Configure logger
    log_filename = f'{datetime.now().isoformat().split(".")[0].replace(":", "-")}.log'
    log_filepath = save_dir.joinpath(log_filename)

    with open(log_filepath, "a") as log_file:
        # Randomly order all possible timestamps
        date_range = list(pd.date_range(start=dates[0], end=dates[1], freq="30min"))
        random.shuffle(date_range)

        # Download images
        home_url = f"https://phenocam.nau.edu/webcam/browse/{site_name}"
        img_template = f"https://phenocam.nau.edu/data/archive/{site_name}"
        n_downloaded = 0

        # Keep downloading until the number downloaded is the number requested
        # or until we are out of dates to sample images from
        while n_downloaded < n_photos and len(date_range) > 0:
            my_datetime = date_range.pop()
            Y = str(my_datetime.year)
            m = str(my_datetime.month).zfill(2)
            D = str(my_datetime.day).zfill(2)
            month_url = f"{home_url}/{Y}/{m}/{D}"
            try:
                resp1 = requests.get(month_url, timeout=10)
            except:
                log_file.write(f"ERROR:Request timed out\n")
                continue
            if resp1.ok:  # Access the archive for the chosen timestamp's month
                arr = resp1.text.split('<span class="imglabel">')[1:]
                success = False
                for a in arr:
                    # Extract the timestamp from provided data
                    nonformatted_timestamp = a.split("&nbsp")[0].strip()
                    index = 0
                    while (nonformatted_timestamp[index] < '0' or nonformatted_timestamp[index] > '9'):
                        index += 1
                    orig_timestamp = nonformatted_timestamp[index:index+8]
                    strip_timestamp = orig_timestamp.replace(":", "")
                    try:
                        pd_timestamp = pd.to_datetime(f"{Y}-{m}-{D} {orig_timestamp}")
                    except:
                        log_file.write(f"WARN:Could not parse {orig_timestamp}\n")
                        break
                    # Find the image within 5 minutes of the chosen timestamp
                    if abs(my_datetime - pd_timestamp) <= pd.Timedelta("5min"):
                        img_fname = f"{site_name}_{Y}_{m}_{D}_{strip_timestamp}.jpg"
                        img_url = f"{img_template}/{Y}/{m}/{img_fname}"
                        output_fpath = save_dir.joinpath(img_fname)
                        if output_fpath.is_file():
                            log_file.write(
                                f"WARN:{img_fname} was already downloaded, skipping\n"
                            )
                            break
                        try:
                            resp2 = requests.get(img_url, timeout=10)
                        except Exception as e:
                            log_file.write(f"ERROR:{e}\n")
                        if resp2.ok:
                            try:
                                img = Image.open(BytesIO(resp2.content))
                                img.save(output_fpath)
                                success = True
                                n_downloaded += 1
                                log_file.write(f"INFO:Retrieved {resp2.url}\n")
                            except:
                                log_file.write(
                                    f"WARN:Could not read or save image from {resp2.url}\n"
                                )
                            break
                        else:
                            log_file.write(f"WARN:Could not reach {resp2.url}\n")
                if not success:
                    log_file.write(
                        f"WARN:Could not find an image within 5 minutes of {str(my_datetime)}\n"
                    )
            else:
                log_file.write(f"WARN:Could not reach {month_url}\n")
    """

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