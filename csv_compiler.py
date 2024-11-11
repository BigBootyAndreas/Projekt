import os
import numpy as np
import time

def csv_compiler(folder_path):

    # List all files in the folder
    files = os.listdir(folder_path)

    # Filter out only the .npz files
    npz_files = [file for file in files if file.endswith(".npz")]

    # the time in the secound column, and the amplitude in the third
    for filename in npz_files:
        full_path = os.path.join(folder_path, filename)
        loaded = np.load(full_path)
        data = loaded["a"]
        csv_filename = filename.replace(".npz", ".csv")
        csv_filepath = os.path.join(folder_path, csv_filename)
        np.savetxt(csv_filepath, data, delimiter=",", fmt="%s", header="Timestamp, Time (s), Amplitude", comments="")
        print(f"Converted {filename}")

def npz_rm(folder_path):

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