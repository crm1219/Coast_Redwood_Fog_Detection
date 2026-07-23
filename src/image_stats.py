import argparse
import cv2
from pathlib import Path
import numpy as np

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("directory")
    parser.add_argument("image_file", help="The directory in which the files are stored")
    parser.add_argument("tif_file", help="The directory in which the files are stored")

    args = parser.parse_args()

    image_dir = Path(args.directory)

    image = cv2.imread(f"{image_dir}/{args.image_file}")
    mask = cv2.imread(f"{image_dir}/{args.tif_file}")

    gaussian = cv2.GaussianBlur(image, (5, 5), 0)
    gray = cv2.cvtColor(gaussian, cv2.COLOR_BGR2GRAY)
    """
    sx = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    sy = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    gradient_magnitude = cv2.magnitude(sx, sy)
    gradient_magnitude = cv2.convertScaleAbs(gradient_magnitude)
    
    #edges = cv2.Canny(gray, 75, 175)
    gradient_x = cv2.filter2D(gray, cv2.CV_64F, sx)
    gradient_y = cv2.filter2D(gray, cv2.CV_64F, sy)

    gradient_direction = np.arctan2(gradient_y, gradient_x) * (180.0 / np.pi)  # in degrees
    gradient_direction[gradient_direction < 0] += 180  # Normalize to [0, 180]

    # Step 5: Non-Maximum Suppression
    height, width = gradient_magnitude.shape
    suppressed_image = np.zeros_like(gradient_magnitude)

    
    for i in range(1, height-1):
        for j in range(1, width-1):
            angle = gradient_direction[i, j]
            
            # Determine the neighboring pixels to compare
            if (0 <= angle < 22.5) or (157.5 <= angle <= 180):
                neighbors = (gradient_magnitude[i, j + 1], gradient_magnitude[i, j - 1])  # Horizontal
            elif (22.5 <= angle < 67.5):
                neighbors = (gradient_magnitude[i + 1, j - 1], gradient_magnitude[i - 1, j + 1])  # Diagonal /
            elif (67.5 <= angle < 112.5):
                neighbors = (gradient_magnitude[i + 1, j], gradient_magnitude[i - 1, j])  # Vertical
            else:
                neighbors = (gradient_magnitude[i - 1, j - 1], gradient_magnitude[i + 1, j + 1])  # Diagonal \
            
            # Suppress non-maxima
            if gradient_magnitude[i, j] >= max(neighbors):
                suppressed_image[i, j] = gradient_magnitude[i, j]
    high_threshold = 100
    low_threshold = 50

    strong_edges = (suppressed_image > high_threshold).astype(np.uint8)
    weak_edges = ((suppressed_image >= low_threshold) & (suppressed_image <= high_threshold)).astype(np.uint8)

    # Final edge image
    final_edges = np.zeros_like(suppressed_image)
    strong_row, strong_col = np.where(strong_edges == 1)

    # Link weak edges to strong edges
    for i in range(len(strong_row)):
        x, y = strong_row[i], strong_col[i]
        # Check 8-connectivity
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if 0 <= x + dx < height and 0 <= y + dy < width:
                    if weak_edges[x + dx, y + dy] == 1:
                        final_edges[x + dx, y + dy] = 255
        final_edges[x, y] = 255  # Keep strong edges
    
        
    cv2.imwrite(f"{args.directory}/{args.image_file.split(".")[0]}_partial_canny.jpg", suppressed_image)
    canny_image = cv2.imread(f"{args.directory}/{args.image_file.split(".")[0]}_partial_canny.jpg")
    final = cv2.bitwise_and(canny_image, mask)
    cv2.imshow("Combined Image", final_edges)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    
    """
    (h, w) = gray.shape
    (cX, cY) = w // 2, h // 2
    fft_shift = np.fft.fftshift(np.fft.fft2(gray))
    r = 40
    fft_shift[cY - r:cY + r, cX - r:cX + r] = 0
    recon = np.fft.ifft2(np.fft.ifftshift(fft_shift))
    magnitude = 20 * np.log(np.abs(recon) + 1e-8)

    cv2.imwrite(f"{args.directory}/{args.image_file.split(".")[0]}_fft.jpg", magnitude)
    canny_image = cv2.imread(f"{args.directory}/{args.image_file.split(".")[0]}_fft.jpg")
    final = cv2.bitwise_and(canny_image, mask)
    print(np.mean(final))
    cv2.imshow("Combined Image", final)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()