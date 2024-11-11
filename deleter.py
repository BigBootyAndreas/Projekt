import os
import numpy as np
import time

# Specify the folder containing the compressed .npz files
folder_path = 'C:\\Users\\Ali\\OneDrive - Aalborg Universitet\\Desktop\\P7\\Data\\data1'

# List all files in the folder
files = os.listdir(folder_path)

# Filter out only the .npz files
npz_files = [file for file in files if file.endswith(".npz")]

# Convert the .npz files to .csv files, saving the timestamp in the first column,
# the time in the second column, and the amplitude in the third
for filename in npz_files:
    full_path = os.path.join(folder_path, filename)
    
    # Remove the .npz file
    os.remove(full_path)
    print(f"Deleted {filename}")
    time.sleep(0.1)