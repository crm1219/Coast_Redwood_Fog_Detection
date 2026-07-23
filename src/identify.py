import os
import argparse
import csv

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("directory")

    args = parser.parse_args()

    data_file_path = f"{args.directory}/Image_Data1.csv"
    data_file = open(f"{args.directory}/Image_Data1.csv", "r")

    data_reader = csv.reader(data_file)
    data = list(data_reader)
    data_file.close()

    for photo in os.scandir(args.directory):
        if photo.is_file() and photo.name.endswith(".jpg"):
            photo_found = False
            for i in range(len(data)):
                if data[i][0] == photo.name:
                    photo_found = True
            if not photo_found:
                print(photo.name)

main()