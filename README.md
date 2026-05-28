# Fog Classification

This program will download a selection of images from a given PhenoCam site, then allow you to classify each image based on how much fog is present. The results will be stored in a .csv file that contains a list of image names and ratings. The program will also create a .txt file storing all the image urls for the given site.

## Usage

Requirements:
* Python 3.10+
* The following Python packages:
    * requests
    * opencv-python
    * pillow

To run this program, enter the following command into the console, with the proper values filled in for each argument:

    python image_classification.py [site_name] [start_date] [end_date] [download_directory] [num_photos]

The start date and end date should be formatted as YYYY/MM/DD, and the download directory should be an absolute filepath to the directory in which you want the images to be stored.

Example Usage:

    python image_classification.py santaluciapreserve1 2020/08/10 2020/12/31 C:/Users/crmos/OneDrive/Documents/Phenocam_Images 2

After the images have been downloaded, the program will open each photo in succession in the lower right corner of the viewport and prompt you to rate them on how much fog is present. The ratings will be recorded in a file titled [site_name]_fogdata.csv. If you run the program multiple times on the same site, new ratings will be added to the same file as opposed to creating a new file.

## Documentation

Please see the file Classification.md in the documentation folder for reference on how to classify images.
