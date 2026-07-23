import argparse
import numpy as np

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("directory", help="The directory containing the files to analyze")

    args = parser.parse_args()

    image_file = open(f"{args.directory}/Image_Data1.csv")
    blur_file = open(f"{args.directory}/Blur_Detection.csv")
    blur_lines = blur_file.readlines()

    # background[clear, light, heavy] midground[clear, light, heavy] foreground[clear, light, heavy]
    focus_values = [[[], [], []], [[], [], []], [[], [], []]]
    totals = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    counts = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    averages = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
    standard_devs = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    index = 0
    for line in image_file:
        if index > 0:
            image_data = line.split(",")
            blur_data = blur_lines[index].split(",")
            if int(image_data[4]) != 7 and int(image_data[4]) != 8 and image_data[0] == blur_data[0]:
                ratings = [int(image_data[1]), int(image_data[2]), int(image_data[3])]
                for i in range(3):
                    totals[i][ratings[i]] += float(blur_data[i + 9])
                    focus_values[i][ratings[i]].append(float(blur_data[i + 9]))
                    counts[i][ratings[i]] += 1
        index += 1

    for i in range(3):
        for j in range(3):
            if counts[i][j] > 0:
                averages[i][j] = totals[i][j] / counts[i][j]

    image_file.close()
    blur_file.close()

    total_correct = 0
    total_wrong = 0

    for i in range(3):
        if i == 0:
            print("Background fog stats:")
        elif i == 1:
            print("Midground fog stats:")
        elif i == 2:
            print("Foreground fog stats:")
        median1 = np.percentile(focus_values[i][0], 75)
        median2 = np.percentile(focus_values[i][1], 25)
        median3 = np.percentile(focus_values[i][1], 75)
        median4 = np.percentile(focus_values[i][2], 25)
        step1 = (median1 - median2) / 100
        step2 = (median3 - median4) / 100
        max_correct = 0
        max_wrong = 0
        max_median_first = median1
        max_median_second = median3
        for k in range(1, 101):
            current_median_first = median1 - k * step1
            for m in range(1, 101):
                current_median_second = median3 - m * step2
                if current_median_second < current_median_first:
                    current_correct = 0
                    current_wrong = 0
                    for l in focus_values[i][0]:
                        if (l > current_median_first):
                            current_correct += 1
                        else: 
                            current_wrong += 1
                    for l in focus_values[i][1]:
                        if (l <= current_median_first and l > current_median_second):
                            current_correct += 1
                        else:
                            current_wrong += 1
                    for l in focus_values[i][2]:
                        if (l <= current_median_second):
                            current_correct += 1
                        else: 
                            current_wrong += 1
                    if current_correct > max_correct:
                        max_correct = current_correct
                        max_median_first = current_median_first
                        max_median_second = current_median_second
                        max_wrong = current_wrong
        print(f"Clear to Light Threshold: {max_median_first}")
        print(f"Light to Heavy Threshold: {max_median_second}")
        print(f"Total correct: {max_correct}")
        print(f"Total wrong: {max_wrong}")
        total_correct += max_correct
        total_wrong += max_wrong

    print(f"\nOverall accuracy: {total_correct / (total_correct + total_wrong)}")

main()