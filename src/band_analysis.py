from PIL import Image
import numpy as np
import sys
from pathlib import Path

def main():
    """image_dir = Path("C:/Users/crmos/OneDrive/Documents/Phenocam_Images/santaluciapreserve1")

    for photo in image_dir.iterdir():
        if photo.is_file():
            print("Content of", f.name, ":")
            print(f.read_text())
    """

    image_path = Path("C:\\Users\\crmos\\OneDrive\\Documents\\Phenocam_Images\\santaluciapreserve1\\santaluciapreserve1_2022_05_16_062949.jpg")
    im = Image.open(image_path)
    im.load()

    mask_path = Path("C:/Users/crmos/Downloads/santaluciapreserve1_EN_1000_01.tif")
    mask_img = Image.open(mask_path)
    roimask = np.asarray(mask_img, dtype=np.bool)

    output = get_roi_stats(im, roimask)


# The key is to identify an object (in my case it is a stand of Eucalyptus in the distance) and create an ROI for that specific location on the image. You can then use a band ratio to identify fog using the green band ratioed over the red band. Under normal circumstances a green tree will produce an elevated Red/Green ratio. However, when fog is present, the red and green bands equalize and the ratio is very different. I have found that approach to be highly effective for day time fog detection. In fact, several student projects from my Geography 175 class comparing fog detects from the fog collector to phenocam detections. However, it does require sunlight and the right scene features. Since the inquiry is about redwoods, I can imagine it should work reasonably well. One might also identify multiple candidate trees or stands and calculate an average to account for potential spatial variation in fog. It does not work for night time detection, but that can be done with a four-channel net radiometer.

def get_roi_stats(im, roimask):
    """
    Function to return a collection of stats for DN values for an image / mask pair.
    """
 
    # split into bands
    (im_r, im_g, im_b) = im.split()

    # create numpy arrays with bands
    r_array = np.asarray(im_r, dtype=np.int16)
    g_array = np.asarray(im_g, dtype=np.int16)

    # try applying mask to red image ... if mask and image don't
    # have same size this will raise an exception.
    try:
        r_ma = np.ma.array(r_array,mask=roimask)
    except:
        errstr = "Error applying mask to image file.\n"
        sys.stderr.write(errstr)
        return None

    # make masked arrays for G,B
    g_ma = np.ma.array(g_array,mask=roimask)

    # find mean, std
    r_vals = r_ma.compressed()
    r_mean = r_vals.mean()

    g_vals = g_ma.compressed()
    g_mean = g_vals.mean()
    
    return r_mean/g_mean
    

main()