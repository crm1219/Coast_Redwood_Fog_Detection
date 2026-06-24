# Allows the user to use a directory of classified images from a PhenoCam site to establish the range of focus values each rating falls into, storing the results in a .csv file

import numpy as np
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("target_dir", help="The directory containing images to use to develop sharpness ranges")
    args = parser.parse_args()
    edge_sharpness(args.target_dir)
        
def edge_sharpness(train_dir):
    """Calculates the range of focus values for each rating at a given site and stores the results in a .csv file.
    
    :param train_dir: The directory containing images and data to use.
    :type train_dir: str
    """

    focus_values = [[], [], [], [], [], [], []]
    data_values = []

    image_data_filepath = f"{train_dir}/Image_Data.csv"
    data_file = open(image_data_filepath)

    range_file = open(f"{train_dir}/Sharpness_Ranges.csv", "w")

    # Check that image data file is present
    if not Path(image_data_filepath).is_file():
        print(f"ERROR: Missing required file 'Image_Data.csv'\n")

    else:
        range_file.write("Rating,Lower Bound,Upper Bound\n")
        
        # Loop through data and add focus values to array
        for line in data_file:
            data = line.split(",")
            if data[0] != "Filename":
                rating = int(data[2])
                if (rating > 0 and rating < 8):
                    focus_values[rating - 1].append(float(data[1]))

        # Calculate 1st and 3rd quartile for focus values for each rating and determine highest rating for a site
        max_rating = 0
        for i in range(7):
            q1 = 0
            q3 = 0
            if len(focus_values[i]) > 0:
                max_rating = i
                q1 = np.percentile(focus_values[i], 25)
                q3 = np.percentile(focus_values[i], 75)
            data_values.append([q1, q3])

        ranges = []

        # Calculate range of focus values for each rating
        for i in range(7):
            lower_bound = 0
            upper_bound = 0
            if i == max_rating:
                lower_bound = -100
            else:
                lower_bound = (data_values[i][0] + data_values[i + 1][1]) / 2
            if i == 0:
                upper_bound = 100
            else:
                upper_bound = (data_values[i][1] + data_values[i - 1][0]) / 2
            ranges.append([lower_bound, upper_bound])

        # Write ranges to csv file
        for i in range(7):
            range_file.write(f"{i + 1},{ranges[i][0]},{ranges[i][1]}\n")

        data_file.close()
        range_file.close()

main()