import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("target_directory", help="The directory to create the new file in")
    parser.add_argument("site_name", help="The PhenoCam site from which the data comes")

    args = parser.parse_args()

    triage_comp(args.target_directory, args.site_name)

def triage_comp(directory, site_name):
    triage_filepath = f"{directory}/ImageTriage.csv"
    data_filepath = f"{directory}/{site_name}_fogdata.csv"

    max_min = [[-100, 100], [-100, 100], [-100, 100], [-100, 100], [-100, 100], [-100, 100], [-100, 100], [-100, 100], [-100, 100]]

    totals = [0, 0, 0, 0, 0, 0, 0, 0]
    counts = [0, 0, 0, 0, 0, 0, 0, 0]
    averages = [0, 0, 0, 0, 0, 0, 0, 0]

    with open(triage_filepath, "r") as triage_file:
        with open(data_filepath, "r") as data_file:
            triage_data = triage_file.readlines()
            index = 1
            for line in data_file:
                rating = int(line.split(",")[1])
                focus = float(triage_data[index].split(",")[0])
                current_max = max_min[int(line.split(",")[1])][0]
                current_min = max_min[int(line.split(",")[1])][1]
                if focus > current_max:
                    max_min[int(line.split(",")[1])][0] = focus
                if focus < current_min:
                    max_min[int(line.split(",")[1])][1] = focus
                totals[rating] += focus
                counts[rating] += 1
                index += 1

    for i in range(8):
        averages[i] = totals[i] / counts[i]
        print(f"Level {i} Average: {averages[i]}")

main()