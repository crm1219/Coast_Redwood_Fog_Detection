import cv2
"""
def sharpness_predict(ranges, test_dir):
    sharpness_file_test = open(f"{test_dir}/edge_sharpness.csv")

    for line in sharpness_file_test:
        data = line.split(",")
        if data[0] != "Filename":
            sharpness_value = float(data[1])
            prediction = 0
            for i in range(7):
                if sharpness_value >= ranges[i][0] and sharpness_value < ranges[i][1]:
                    prediction = i + 1

image_path = f"{train_dir}/{data[0]}"
                brightness = compute_brightness(image_path)
                brightness_values[rating].append(brightness)

        for i in range(9):
            if len(brightness_values[i]) > 0:
                averages[i] = sum(brightness_values[i]) / len(brightness_values[i])
            print(f"Average brightness for rating {i}: {averages[i]}")

def compute_brightness(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    average_brightness = np.mean(gray)
    return average_brightness
"""