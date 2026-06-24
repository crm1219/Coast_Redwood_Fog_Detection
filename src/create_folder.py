import cv2 as cv
import shutil
import os
import random

def main():
    srl_sites = ["centralredwoods1", "centralredwoods2", "delnortecounty1", "delnortecounty2", "santacruz1", "santacruz2", "santaluciapreserve1", "santaluciapreserve2"]

    site_names = ["centralredwoods1", "centralredwoods2", "delnortecounty1", "delnortecounty2", "santacruz1", "santacruz2", "santaluciapreserve1", "santaluciapreserve2"]

    for i in range(0, 8):
        print(f"Copying over images for {srl_sites[i]}!")
        copy_images(srl_sites[i], site_names[i])

    print("Renaming image files!")
    rename()


def copy_images(folder_name, site):
    im_directory = f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/{folder_name}"
    new_directory = f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/srlsites"
    csv_filename = f"{new_directory}/srlsites_fogdata.csv"

    csv_file = open(csv_filename, "a")

    dark_images = []
    clear_images = []
    light_fog_images = []
    heavy_fog_images = []

    kept_images = []

    with open(f"{im_directory}/{site}_fogdata.csv") as data_file:
        for line in data_file:
            if line.split(",")[1] == "0\n":
                dark_images.append((line.split(",")[0], line.split(",")[1]))
            elif line.split(",")[1] == "1\n":
                clear_images.append((line.split(",")[0], line.split(",")[1]))
            elif line.split(",")[1] == "2\n" or line.split(",")[1] == "3\n":
                light_fog_images.append((line.split(",")[0], line.split(",")[1]))
            else:
                heavy_fog_images.append((line.split(",")[0], line.split(",")[1]))

    get_images(len(dark_images), dark_images, kept_images)
    get_images(50, clear_images, kept_images)
    get_images(len(light_fog_images), light_fog_images, kept_images)
    get_images(len(heavy_fog_images), heavy_fog_images, kept_images)

    for image in kept_images:
        image_name = image[0]
        image_rating = image[1]
        image_location = f"{im_directory}/{image_name}"
        shutil.copy(image_location, new_directory)
        csv_file.write(f"{image_name},{image_rating}")

    csv_file.close()

def rename():
    folder_path = "C:/Users/crmos/OneDrive/Documents/Phenocam_Images/srlsites"
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