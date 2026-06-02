from PIL import Image
import cv2
import numpy as np
import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("site_name", help="The PhenoCam site from which the data comes")

    args = parser.parse_args()

    image_dir = f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/{args.site_name}"

    focus_values = [[], [], [], [], [], [], [], []]

    averages = [0, 0, 0, 0, 0, 0, 0, 0]
    standard_devs = [0, 0, 0, 0, 0, 0, 0]

    with open(f"{image_dir}/{args.site_name}_fogdata.csv") as data_file:
        for line in data_file:
            data = line.split(",")
            im_path = f"{image_dir}/{data[0]}"
            output = compute_blur_fft(im_path)
            rating = int(data[1])
            focus_values[rating].append(output)

    for i in range(8):
        if (len(focus_values[i]) > 0):
            averages[i] = sum(focus_values[i] / len(focus_values[i]))
        else:
            averages[i] = 0


def compute_blur_fft(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    (h, w)      = gray.shape
    (cX, cY)    = w // 2, h // 2
    fft_shift = np.fft.fftshift(np.fft.fft2(gray))
    r         = 40
    fft_shift[cY - r:cY + r, cX - r:cX + r] = 0
    recon     = np.fft.ifft2(np.fft.ifftshift(fft_shift))
    magnitude = 20 * np.log(np.abs(recon) + 1e-8)
    return float(np.mean(magnitude))

main()