from pathlib import Path
import cv2
import numpy as np
import argparse
import os

def main():
    parser = argparse.ArgumentParser(description="Generate predictions for fog quantity in a single image or a directory of images")

    parser.add_argument("method", help="The prediction method to use")
    parser.add_argument("directory", help="The directory of images to generate predictions for")
    parser.add_argument("--range_file", default="", help="The .csv file to use to generate predictions using edge sharpness - required for the method of edge sharpness")
    parser.add_argument("--classification", default="csv", help="The classification method to use - either csv to store the results in a .csv file or directory to sort images into separate folders")

    args = parser.parse_args()

    if args.method == "edge_sharpness":
        if args.range_file == "":
            print("ERROR: Range file must be provided if using the edge sharpness prediction method.")
        else:
            sharpness_predict(args.directory, args.range_file, args.classification)

def sharpness_predict(directory, range_filepath, classification):
    """Predicts the fog classification for images in a directory using edge sharpness.
    
    :param directory: The directory containing images to classify.
    :type directory: str
    :param directory: The directory containing images to classify.
    :type directory: str
    :param directory: The directory containing images to classify.
    :type directory: str"""
    # Check to make sure given file exists
    if not Path(range_filepath).is_file():
        print("ERROR: Provided range file does not exist, or filepath is invalid")
        return
    
    # Append range values to array
    ranges = []
    with open(f"{range_filepath}") as range_file:
        for line in range_file:
            data = line.split(",")
            if data[0] != "Rating":
                ranges.append([int(data[0]), float(data[1]), float(data[2])])

    # Create csv file if classification method is csv
    if (classification == "csv"):
        prediction_file = open(f"{directory}/sharpness_predictions.csv", "w")
        prediction_file.write("Filename,Brightness,Focus Value,Prediction\n")
    # Otherwise, create directories to store classified images in
    elif (classification == "directory"):
        for i in range(8):
            directory_path = Path(f"{directory}/{i}")
            try:
                directory_path.mkdir()
            except FileExistsError:
                print(f"ERROR: Directory '{directory_path}' already exists.")
            except PermissionError:
                print(f"ERROR: Permission denied: Unable to create '{directory_path}'.")
            except Exception as e:
                print(f"ERROR: An error occurred: {e}")
    else:
        print("ERROR: Classification method is invalid")
        return

    directory_path = Path(f"{directory}")

    # Loop through images in given directory
    for photo in directory_path.iterdir():
        if photo.is_file():
            if photo.name.endswith("jpg"):
                # Compute blur and brightness
                img = cv2.imread(f"{directory}/{photo.name}")
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                brightness = compute_brightness(gray)
                blur = compute_blur_fft(gray)
                # Classify images that are too dark
                if brightness <= 40:
                    if (classification == "csv"):
                        prediction_file.write(f"{photo.name},{brightness},{blur},0\n")
                    elif (classification == "directory"):
                        old_path = os.path.join(directory, photo.name)
                        new_path = os.path.join(f"{directory}/0", photo.name)
                        os.rename(old_path, new_path)
                # Otherwise, find the appropriate range into which the image falls
                else:
                    prediction = 0
                    for i in range(7):
                        if blur >= ranges[i][1] and blur <= ranges[i][2]:
                            prediction = i + 1
                            if (classification == "csv"):
                                prediction_file.write(f"{photo.name},{brightness},{blur},{prediction}\n")
                            elif (classification == "directory"):
                                old_path = os.path.join(directory, photo.name)
                                new_path = os.path.join(f"{directory}/{prediction}", photo.name)
                                os.rename(old_path, new_path)
    
    if (classification == "csv"):
        prediction_file.close()
    

def compute_brightness(gray):
    """Computes the average brightness of an image using numpy mean.
    
    :param gray: A grayscale version of the image to be analyzed.
    :type gray: numpy array"""
    average_brightness = np.mean(gray)
    return average_brightness

def compute_blur_fft(gray):
    """Computes the amount of blur in an image using a Fast Fourier transform.
    
    :param gray: A grayscale version of the image to be analyzed.
    :type gray: numpy array"""
    (height, width) = gray.shape
    (cX, cY) = width // 2, height // 2
    fft_shift = np.fft.fftshift(np.fft.fft2(gray))
    radius = 40
    fft_shift[cY - radius:cY + radius, cX - radius:cX + radius] = 0
    recon = np.fft.ifft2(np.fft.ifftshift(fft_shift))
    magnitude = 20 * np.log(np.abs(recon) + 1e-8)
    return float(np.mean(magnitude))

main()