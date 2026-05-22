# Fog Classification

This program will download a selection of images from a given PhenoCam site, then allow you to classify each image based on how much fog is present. The results will be stored in a .csv file that contains a list of image names and ratings.

## Usage

To run this program, enter the following command into the console, with the proper values filled in for each argument:

python image_classification.py [site_name] [start_date] [end_date] [download_directory] [num_photos]

The start date and end date should be formatted as YYYY/MM/DD, and the download directory should be an absolute filepath to the directory in which you want the images to be stored.

After the images have been downloaded, the program will open each photo in succession in the lower right corner of the viewport and prompt you to rate them on how much fog is present. The results will be stored in a .csv file created in the same directory as the images, titled [site_name]_fogdata.csv.

## Documentation

Please see the file Classification.md in the documentation folder for reference on how to classify images.
