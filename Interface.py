import os
from AnalysisAcoustic import perform_fft_analysis  # import
from npz_cleaner import npz_rm
from csv_compiler import csv_compiler
from IMU import IMU_analysis
from IMU import plot_psd_data
from IMU import plot_unprocessed_data
from segmentation_loop import segmentation_analysis

# Variables
###################################################


#Interface inputs
yes = {'yes', 'y', 'ye', ''}
no = {'no', 'n'}

# Segmentation:
sample_rate = 16000         # Data sample rate (Hz)
window_samples = 5          # window size, should match sample size (s)
step_size = 1               # Incremnts between each window scan (s)
sample_dir = 'samples\\'    # Sample directory (default: 'samples\\')
output_dir = 'results\\'    # Output directory (default: 'results\\')
amp_tol = 0.0002            # Amplitude tolerance (default: 0.0002)
amp_var_tol = 0.0002        # Amplitude variance tolerance (default: 0.0002)

###################################################

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
    file_choice = []
    k = 0
    while True:
        choice = int(input("Enter the number corresponding to the file: ")) - 1
        if k >= 1:
            if 0 <= choice < len(imu_files):
                if choice in file_choice:
                    print("File already seleceted")
                    if input("Are you done? (y/n)").lower() in yes:
                        break
                else: 
                    file_choice.append(choice)
                    if input("Are you done? (y/n)").lower() in yes:
                        break
        elif k == 0:
            if 0 <= choice < len(imu_files):
                file_choice.append(choice)
                if input("Are you done? (y/n)").lower() in yes:
                    break
                k += 1
        else:
            print("Invalid selection. Please choose a valid file number.")
      


    # Create file paths based on user choices
    file_path = []
    for i in range(len(file_choice)):
        selected_file = imu_files[file_choice[i]]
        full_path = os.path.join(imu_directory, selected_file)
        file_path.append(full_path)
        print(f"Processing file: {selected_file}")
    imu_choise=[]
    while True:
        imu_choise=input ("Enter '1' for Unprocessed data or '2' for Processed data:")
        if imu_choise == '1':
            print("Unprocessed data is being plotted")
            IMU_analysis(file_path,file_choice,'unprocessed')
            break
        elif imu_choise=='2':
            print("Processed data is being plotted")
            IMU_analysis(file_path,file_choice,'psd')
            break



def acoustic(directory):

    print("Welcome to the Acoustic analysis tool.")
    
    run = True

    # List subdirectories in the Acoustic directory
    subdirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]

    if not subdirs:
        print("No subdirectories found in the Acoustic directory.")
        return
    
    while True:
        
        print("Available subfolders for Acoustic analysis:")
        for idx, subdir in enumerate(subdirs):
            print(f"{idx + 1}. {subdir}")

        sub_choice = int(input("Enter the number corresponding to the subfolder: ")) - 1
            
        if 0 <= sub_choice < len(subdirs):
            selected_subdir = subdirs[sub_choice]
            subdir_path = os.path.join(directory, selected_subdir)
            print(f"You selected {selected_subdir}. Full path: {subdir_path}")
            
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
            analysis_choice = input("1. FFT analysis\n2. Segment analysis\n")

            if analysis_choice == '1':  # FFT

                # Perform the FFT analysis on the selected subdirectory
                perform_fft_analysis(subdir_path)
                break

            elif analysis_choice == '2':  # Segmentation
                    
                # Perform segmentation analysis
                segmentation_analysis(subdir_path,window_samples, step_size, sample_rate, sample_dir, output_dir, amp_tol, amp_var_tol)

            else:
                print("Invalid selection. Please restart and choose '1' or '2'.")

        else:
            print("Invalid selection. Please restart and choose a valid subfolder.")
        
        run_again = input("Run again? (y/n): ").strip().lower()
        if run_again not in yes:
            print("Exiting the program.")
            break

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
