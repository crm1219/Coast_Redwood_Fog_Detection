import argparse

def main():
    category_list = ["dark", "clear", "light", "moderate", "heavy"]

    parser = argparse.ArgumentParser()

    parser.add_argument("target_directory", help="The directory to create the new file in")
    parser.add_argument("site_name", help="The PhenoCam site from which the data comes")

    args = parser.parse_args()

    csv_file = f"{args.target_directory}/Image_Data.csv"
    save_to = f"{args.target_directory}/labels.csv"

    save_to_file = open(save_to, "w")
    save_to_file.write(f"# Site: {args.site_name}\n# Categories:\n")

    for i in range(len(category_list)):
        save_to_file.write(f"# {i}. {category_list[i]}\n")

    save_to_file.write("timestamp,label\n")

    with open(csv_file, "r") as data_file:
        for line in data_file:
            array = line.split(",")
            if array[0] != "Filename":
                date = (array[0].split("."))[0]
                timestamp_arr = date.split("_")
                timestamp = "-".join(timestamp_arr[1:4])
                hms = timestamp_arr[-1]
                timestamp += f" {hms[:2]}:{hms[2:4]}:{hms[4:]}"
                category = ""
                if int(array[1]) == 0:
                    category = "clear"
                elif int(array[1]) == 1:
                    category = "light"
                elif int(array[1]) == 2 or int(array[1]) == 3:
                    category = "moderate"
                elif int(array[1]) == 4 or int(array[1]) == 5 or int(array[1]) == 6:
                    category = "heavy"
                elif int(array[1]) == 7:
                    category = "dark"
                save_to_file.write(f"{timestamp},{category}\n")

    save_to_file.close()

main()