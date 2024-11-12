import os
from AnalysisAcoustic import perform_fft_analysis  # import
from npz_cleaner import npz_rm
from csv_compiler import csv_compiler
from IMU import IMU_analysis
from segmentation_loop import segmentation_analysis

# Predefined paths for each person
person_paths = {
    'Ali': r'C:\\Users\\Ali\\OneDrive - Aalborg Universitet\\Desktop\\P7\\Data\\',
    'Sofus': r'C:\\Users\\bemme\\Downloads\\data\\',
    'Dipendra': 'C:\\Users\\Person3\\Downloads\\data\\',
    'Theis': 'C:\\Users\\Person4\\Downloads\\data\\',
    'Zahid': 'C:\\Users\\Person5\\Downloads\\data\\',
}

def IMU(directory):
    print("Welcome to the IMU analysis tool.")
    
    # Navigate to the 'IMU' subdirectory
    imu_directory = os.path.join(directory, 'IMU')
    if not os.path.exists(imu_directory):
        print("IMU directory not found in the specified path.")
        return

    # List all CSV files in the IMU directory
    imu_files = [f for f in os.listdir(imu_directory) if f.endswith('.csv')]

    if not imu_files:
        print("No CSV files found in the IMU directory.")
        return

    print("Files available for IMU analysis:")
    for idx, file in enumerate(imu_files):
        print(f"{idx + 1}. {file}")

    # Let the user select a file
    file_choice = int(input("Enter the number corresponding to the file: ")) - 1

    if 0 <= file_choice < len(imu_files):
        selected_file = imu_files[file_choice]
        file_path = os.path.join(imu_directory, selected_file)
        print(f"Processing file: {selected_file}")
        
        # Call the IMU analysis function with the selected file path
        IMU_analysis([], file_path)
    else:
        print("Invalid selection. Please restart and choose a valid file number.")


def acoustic(directory):
    print("Welcome to the Acoustic analysis tool.")
    
    # List subdirectories in the Acoustic directory
    subdirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    if not subdirs:
        print("No subdirectories found in the Acoustic directory.")
        return

    print("Available subfolders for Acoustic analysis:")
    for idx, subdir in enumerate(subdirs):
        print(f"{idx + 1}. {subdir}")

    sub_choice = int(input("Enter the number corresponding to the subfolder: ")) - 1

    if 0 <= sub_choice < len(subdirs):
        selected_subdir = subdirs[sub_choice]
        subdir_path = os.path.join(directory, selected_subdir)
        print(f"You selected {selected_subdir}. Full path: {subdir_path}")
        
        # Ask if conversion is wanted
        yes = {'yes', 'y', 'Y', 'ye', ''}
        no = {'no', 'n'}

        convert = input("Would you like to convert the files? (y/n)").lower()
        if convert in yes:
            csv_compiler(subdir_path)
            npz_rm(subdir_path)
            print("Files converted to CSV and npz files deleted.")
        elif convert in no:
            print("Files already CSV.")
        else:
            print("Please respond with 'yes' or 'no'.")

        print("Choose which analysis you want to conduct")
        analysis_choice = input("Enter '1' for FFT analysis or '2' for segment analysis: ")

        if analysis_choice == '1':  # FFT

            # Perform the FFT analysis on the selected subdirectory
            perform_fft_analysis(subdir_path)

        elif analysis_choice == '2':  # Segmentation
            
            # Perform segmentation analysis
            segmentation_analysis(subdir_path)

        else:
            print("Invalid selection. Please restart and choose '1' or '2'.")
    else:
        print("Invalid selection. Please restart and choose a valid subfolder.")

def main():
    print("Welcome to data processing")
    print("Please choose between Acoustic and IMU")
    analysis_choice = input("Enter '1' for Acoustic analysis or '2' for IMU analysis: ")

    persons = list(person_paths.keys())
    for idx, person in enumerate(persons):
        print(f"{idx + 1}. {person}")
    
    choice = int(input("Enter the number corresponding to your name: ")) - 1

    if 0 <= choice < len(persons):
        selected_person = persons[choice]
        base_directory = person_paths[selected_person]
        print(f"You selected {selected_person}. Data directory: {base_directory}")

        if analysis_choice == '1':  # Acoustic analysis
            acoustic_directory = os.path.join(base_directory, 'Acoustic')
            acoustic(acoustic_directory)
        elif analysis_choice == '2':  # IMU analysis
            IMU(base_directory)
        else:
            print("Invalid selection. Please restart and choose '1' or '2'.")
    else:
        print("Invalid selection. Please restart and choose a valid person number.")

if __name__ == "__main__":
    main()
