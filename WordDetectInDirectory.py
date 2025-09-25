import os
import shutil

# Inputs
directory_path = input("Enter the absolute path of the folder: ")
detect_this = input("Enter the word you want to detect in the files: ")
if f"Flagged_{detect_this}" not in os.listdir(directory_path):
    os.mkdir(f"Flagged_{detect_this}")
files = os.listdir(directory_path)
files.remove(f"Flagged_{detect_this}")
files.remove("detector.py")
flagged_files = []
for file in files:
    with open(file, "r") as f:
        if detect_this.lower() in f.read().lower():
            flagged_files.append(file)
for file in flagged_files:
    shutil.move(directory_path+file, directory_path +
                "Flagged_"+detect_this)


print(
    f"The script was successfull in detecting {detect_this} in the list of files")
print(" ")
print("Summary of the detection: ")
print(f"Total Files: {len(files)}")
print(f"Files with the target word: {len(flagged_files)}")
print(" ")
print("Thanks for using this script..........")
