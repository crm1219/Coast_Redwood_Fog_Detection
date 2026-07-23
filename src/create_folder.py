import cv2 as cv
import shutil
import os
import random
from pathlib import Path

def main():
    srl_sites = ["centralredwoods1test", "centralredwoods2test", "delnortecounty1test", "delnortecounty2test", "santacruz1test", "santacruz2test", "santaluciapreserve1test", "santaluciapreserve2test"]

    #csv_file = open("C:/Users/crmos/OneDrive/Documents/Phenocam_Images/srlsitestest/Image_Data.csv", "a")
    #csv_file.write("Filename,Total Rating,\n")

    #for i in range(0, 8):
    #    print(f"Copying over images for {srl_sites[i]}!")
    #    copy_images(srl_sites[i])

    print("Renaming image files!")
    rename()

    #csv_file.close()


def copy_images(folder_name):
    im_directory = f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/{folder_name}"
    new_directory = f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/srlsitestest"
    csv_filename = f"{new_directory}/Image_Data.csv"

    csv_file = open(csv_filename, "a")

    dark_images = []
    clear_images = []
    light_fog_images = []
    heavy_fog_images = []

    kept_images = []

    with open(f"{im_directory}/Image_Data1.csv") as data_file:
        for line in data_file:
            if line.split(",")[0] != "Filename":
                if int(line.split(",")[4]) == 7:
                    dark_images.append((line.split(",")[0], int(line.split(",")[4])))
                elif int(line.split(",")[4]) == 0:
                    clear_images.append((line.split(",")[0], int(line.split(",")[4])))
                elif int(line.split(",")[4]) == 1 or int(line.split(",")[4]) == 2:
                    light_fog_images.append((line.split(",")[0], int(line.split(",")[4])))
                elif int(line.split(",")[4]) != 8:
                    heavy_fog_images.append((line.split(",")[0], int(line.split(",")[4])))

    get_images(len(dark_images), dark_images, kept_images)
    get_images(len(clear_images), clear_images, kept_images)
    get_images(len(light_fog_images), light_fog_images, kept_images)
    get_images(len(heavy_fog_images), heavy_fog_images, kept_images)

    for image in kept_images:
        image_name = image[0]
        image_rating = image[1]
        image_location = f"{im_directory}/{image_name}"
        shutil.copy(image_location, new_directory)
        csv_file.write(f"{image_name},{image_rating}\n")

    csv_file.close()

def rename():
    folder_path = "C:/Users/crmos/OneDrive/Documents/Phenocam_Images/srlsitestest"
    for filename in os.listdir(folder_path):
        if filename.endswith('.jpg') and not filename.startswith("srlsites"):
            index = 0
            letter = filename[index]
            while letter != "_":
                index += 1
                letter = filename[index]
            suffix = filename[index:]
            new_filename = "srlsites" + suffix
            old_path = os.path.join(folder_path, filename)
            new_path = os.path.join(folder_path, new_filename)
            os.rename(old_path, new_path)

def get_images(num_images, image_list, all_images):
    index = 0
    while index < num_images:
        current_image = random.choice(image_list)
        if not current_image in all_images:
            all_images.append(current_image)
            index += 1

main()