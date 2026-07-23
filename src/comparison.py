import argparse
import numpy as np

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("method", help="The method to evaluate")
    parser.add_argument("site_name", help="The PhenoCam site from which the data comes")
    parser.add_argument("train_directory", help="The directory storing training data")
    parser.add_argument("test_directory", help="The directory storing testing data")

    args = parser.parse_args()

    if args.method == "phenocam_snow":
        phenocamsnow_comp(args.test_directory)
    elif args.method == "edge_sharpness":
        sharpness_predict(args.test_directory)

def phenocamsnow_comp(directory):
    labels = f"{directory}/labels.csv"
    predictions = f"{directory}/predictions.csv"

    total = 0
    accurate = 0
    index = 0
    clear_light = 0
    light_clear = 0
    light_heavy = 0
    heavy_light = 0
    clear_heavy = 0
    heavy_clear = 0

    labels_file = open(labels, "r")
    predictions_file = open(predictions, "r")
    predictions_text = predictions_file.readlines()

    for line in labels_file:
        if index > 10:
            total += 1
            label = line.split(",")[1]
            prediction = predictions_text[index].split(",")[1]
            if label == prediction:
                accurate += 1
            else:
                print(f"{label} mislabelled as {prediction} for {line.split(",")[0]}")
            """
            elif (label == "clear\n" and prediction == "light_fog\n"):
                clear_light += 1
                print(f"{line.split(",")[0]} - Clear mislabelled as light fog")
            elif (label == "light_fog\n" and prediction == "clear\n"):
                light_clear += 1 
                print(f"{line.split(",")[0]} - Light fog mislabelled as clear")
            elif (label == "light_fog\n" and prediction == "heavy_fog\n"):
                light_heavy += 1 
                print(f"{line.split(",")[0]} - Light fog mislabelled as heavy fog")
            elif (label == "heavy_fog\n" and prediction == "light_fog\n"):
                heavy_light += 1
                print(f"{line.split(",")[0]} - Heavy fog mislabelled as light fog")
            elif (label == "heavy_fog\n" and prediction == "clear\n"):
                heavy_clear += 1
                print(f"{line.split(",")[0]} - Heavy fog mislabelled as clear")
            elif (label == "clear\n" and prediction == "heavy_fog\n"):
                clear_heavy += 1
                print(f"{line.split(",")[0]} - Clear mislabelled as heavy fog")
            """
            
        index += 1

    print(f"Total images: {total}")
    print(f"Accurate predictions: {accurate}")
    print(f"Clear images mislabelled as light fog: {clear_light}")
    print(f"Light fog images mislabelled as clear: {light_clear}")
    print(f"Light fog images mislabelled as heavy fog: {light_heavy}")
    print(f"Heavy fog images mislabelled as light fog: {heavy_light}")
    print(f"Clear images mislabelled as heavy fog: {clear_heavy}")
    print(f"Heavy fog images mislabelled as clear: {heavy_clear}")

    labels_file.close()
    predictions_file.close()

def sharpness_predict(test_dir):
    sharpness_file = open(f"{test_dir}/Sharpness_Ranges.csv")
    image_file = open(f"{test_dir}/Image_Data1.csv")
    total = 0
    calculations = [0, 0, 0, 0, 0, 0, 0]
    ranges = []
    for line in sharpness_file:
        data = line.split(",")
        if data[0] != "Rating":
            ranges.append([float(data[1]), float(data[2])])

    for line in image_file:
        data = line.split(",")
        if data[0] != "Filename":
            sharpness_value = float(data[1])
            prediction = 0
            for i in range(7):
                if sharpness_value >= ranges[i][0] and sharpness_value < ranges[i][1]:
                    prediction = i + 1
            rating = int(data[2])
            if rating != 0 and rating != 8:
                total += 1
                
                """
                if (rating == 1 and prediction == 1) or (rating in [2, 3] and prediction in [2, 3]) or (rating in [4, 5, 6, 7] and prediction in [4, 5, 6, 7]):
                    calculations[0] += 1
                elif (rating == 1 and prediction in [2, 3]):
                    calculations[1] += 1
                elif (rating in [2, 3] and prediction == 1):
                    calculations[2] += 1
                elif (rating in [2, 3] and prediction in [4, 5, 6, 7]):
                    calculations[3] += 1
                elif (rating in [4, 5, 6, 7] and prediction in [2, 3]):
                    calculations[4] += 1
                elif (rating == 1 and prediction in [4, 5, 6, 7]):
                    calculations[5] += 1
                else:
                    calculations[6] += 1
                """
                if rating == prediction:
                        calculations[0] += 1
                elif (rating == prediction + 1) or (rating == prediction - 1):
                    calculations[1] += 1
                elif (rating == prediction + 2) or (rating == prediction - 2):
                    calculations[2] += 1
                elif (rating == prediction + 3) or (rating == prediction - 3):
                    calculations[3] += 1
                elif (rating == prediction + 4) or (rating == prediction - 4):
                    calculations[4] += 1
                elif (rating == prediction + 5) or (rating == prediction - 5):
                    calculations[5] += 1
                else:
                    calculations[6] += 1

    """
    print(f"Total images: {total}")
    print(f"Accurate predictions: {calculations[0]}")
    print(f"Clear images mislabelled as light fog: {calculations[1]}")
    print(f"Light fog images mislabelled as clear: {calculations[2]}")
    print(f"Light fog images mislabelled as heavy fog: {calculations[3]}")
    print(f"Heavy fog images mislabelled as light fog: {calculations[4]}")
    print(f"Clear images mislabelled as heavy fog: {calculations[5]}")
    print(f"Heavy fog images mislabelled as clear: {calculations[6]}")
    """
    print(f"Total images: {total}")
    for i in range(6):
        print(f"Images off by {i}: {calculations[i]}")
    print(f"Images off by 6+: {calculations[6]}")
    

    sharpness_file.close()
    image_file.close()

main()