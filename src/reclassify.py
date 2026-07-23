import os
import cv2 as cv
import argparse

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("site_name", help="The site to draw images from")

    args = parser.parse_args()

    reclassify(args.site_name)

def reclassify(site_name):
    directory = "C:/Users/crmos/OneDrive/Documents/Phenocam_Images/statisticstest"
    #csv_file1 = open(f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/{site_name}/Image_Data.csv", "r")
    #csv_file2 = open(f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/{site_name}test/Image_Data.csv", "r")
    new_file1 = open(f"{directory}/Image_Data1.csv", "w")
    #new_file2 = open(f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/{site_name}test/Image_Data1.csv", "w")

    new_file1.write("Filename,Background Fog,Midground Fog,Foreground Fog,\n")
    #new_file2.write("Filename,Background Fog,Midground Fog,Foreground Fog,\n")

    for photo in os.scandir(directory):
        if photo.is_file() and photo.name.endswith(".jpg"):
            image_location = f"{directory}/{photo.name}"
            img = cv.imread(image_location)

            # Resize and move image so it can be displayed side by side with the terminal window
            resized_image = cv.resize(img, (778, 576))
            cv.imshow(photo.name, resized_image)
            cv.moveWindow(photo.name, 700, 250)
            cv.waitKey(1)

            # Collect user input for level of fogginess and record in .csv file
            user_input1 = input("Enter level of background fogginess: ")
            while (user_input1 < "0" or user_input1 > "3"):
                user_input1 = input("Please enter a number between 0 and 3: ")
        
            user_input2 = input("Enter level of midground fogginess: ")
            while (user_input2 < "0" or user_input2 > "3"):
                user_input2 = input("Please enter a number between 0 and 3: ")
            
            user_input3 = input("Enter level of foreground fogginess: ")
            while (user_input3 < "0" or user_input3 > "3"):
                user_input3 = input("Please enter a number between 0 and 3: ")
            
            total = 0
            if user_input1 == "3" or user_input2 == "3" or user_input3 == "3":
                total = 8
            else:
                total = int(user_input1) + int(user_input2) + int(user_input3)
            
            new_file1.write(f"{photo.name},{int(user_input1)},{int(user_input2)},{int(user_input3)},{total},\n")

            cv.destroyAllWindows()
            cv.waitKey(1) 

            
    """
    for line in csv_file1:
        if index != 0:
            photo_name = line.split(",")[0]
            rating = line.split(",")[1]
            if int(rating) == 0:
                new_file1.write(f"{photo_name},7,7,7,7,\n")
            elif int(rating) == 1:
                new_file1.write(f"{photo_name},0,0,0,0,\n")
            else:
                image_location = f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/{site_name}test/{photo_name}"
                img = cv.imread(image_location)

                # Resize and move image so it can be displayed side by side with the terminal window
                resized_image = cv.resize(img, (778, 576))
                cv.imshow(photo_name, resized_image)
                cv.moveWindow(photo_name, 700, 250)
                cv.waitKey(1)

                # Collect user input for level of fogginess and record in .csv file
                user_input1 = input("Enter level of background fogginess: ")
                while (user_input1 < "0" or user_input1 > "3"):
                    user_input1 = input("Please enter a number between 0 and 3: ")
            
                user_input2 = input("Enter level of midground fogginess: ")
                while (user_input2 < "0" or user_input2 > "3"):
                    user_input2 = input("Please enter a number between 0 and 3: ")
                
                user_input3 = input("Enter level of foreground fogginess: ")
                while (user_input3 < "0" or user_input3 > "3"):
                    user_input3 = input("Please enter a number between 0 and 3: ")
                
                total = 0
                if user_input1 == "3" or user_input2 == "3" or user_input3 == "3":
                    total = 8
                else:
                    total = int(user_input1) + int(user_input2) + int(user_input3)
                
                new_file1.write(f"{photo_name},{int(user_input1)},{int(user_input2)},{int(user_input3)},{total},\n")

                cv.destroyAllWindows()
                cv.waitKey(1) 
        index += 1

    index = 0
    for line in csv_file2:
        if index != 0:
            photo_name = line.split(",")[0]
            rating = line.split(",")[2]
            if int(rating) == 0:
                new_file2.write(f"{photo_name},dark,dark,dark,\n")
            elif int(rating) == 1:
                new_file2.write(f"{photo_name},clear,clear,clear,\n")
            else:
                image_location = f"C:/Users/crmos/OneDrive/Documents/Phenocam_Images/{site_name}test/{photo_name}"
                img = cv.imread(image_location)

                # Resize and move image so it can be displayed side by side with the terminal window
                resized_image = cv.resize(img, (778, 576))
                cv.imshow(photo_name, resized_image)
                cv.moveWindow(photo_name, 700, 250)
                cv.waitKey(1)

                # Collect user input for level of fogginess and record in .csv file
                user_input1 = input("Enter level of background fogginess: ")
                while (user_input1 < "0" or user_input1 > "4"):
                    user_input1 = input("Please enter a number between 0 and 4: ")
            
                user_input2 = input("Enter level of midground fogginess: ")
                while (user_input2 < "0" or user_input2 > "4"):
                    user_input2 = input("Please enter a number between 0 and 4: ")
                
                user_input3 = input("Enter level of foreground fogginess: ")
                while (user_input3 < "0" or user_input3 > "4"):
                    user_input3 = input("Please enter a number between 0 and 4: ")
                
                new_file2.write(f"{photo_name},{ratings_list[int(user_input1)]},{ratings_list[int(user_input2)]},{ratings_list[int(user_input3)]}\n")
                
                cv.destroyAllWindows()
                cv.waitKey(1) 
        index += 1
    """
    #csv_file1.close()
    #csv_file2.close()
    new_file1.close()
    #new_file2.close()

main()

