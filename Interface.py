import os
from AnalysisAcoustic import perform_fft_analysis 
from AnalysisAcoustic import plot_raw_data
from npz_cleaner import npz_rm
from csv_compiler import csv_compiler
from IMU import IMU_analysis
from segmentation_loop import segmentation_analysis
from linearregression import plot_scatter
from RMS import plot_rms
from itertools import cycle

# Variables
###################################################

# IMU
wavelet_type = 'db4'       # Wavelet type
level = 5                   # Wavelet level

colors = cycle(['red', 'blue', 'green', 'lawngreen', 'magenta', 'orange'])
alt_color = cycle(['red', 'lawngreen', 'blue', 'magenta', 'green', 'orange'])

# Segmentation:
sample_rate = 16000         # Data sample rate (Hz)
window_samples = 5          # window size, should match sample size (s)
step_size = 1               # Incremnts between each window scan (s)
sample_dir = 'samples\\'    # Sample directory (default: 'samples\\')
output_dir = 'results\\'    # Output directory (default: 'results\\')
amp_tol = 0.0002            # Amplitude tolerance (default: 0.0002)
amp_var_tol = 0.0002        # Amplitude variance tolerance (default: 0.0002)

# Interface inputs
yes = {'yes', 'y', 'ye', ''}
no = {'no', 'n'}

###################################################

# Predefined paths for each person
person_paths = {
    'Ali': r'C:\\Users\\Ali\\OneDrive - Aalborg Universitet\\Desktop\\P7\\Data\\',
    'Sofus': r'C:\\Users\\bemme\\Downloads\\data\\',
    'Dipendra': 'C:\\Users\\Person3\\Downloads\\data\\',
    'Theis': 'C:\\Users\\Person4\\Downloads\\data\\',
    'Zahid': 'C:\\Users\\Person5\\Downloads\\data\\',
}

def IMU(directory, wavelet_type, level, colors, alt_color):
    print("Welcome to the IMU analysis tool.")
    
    while True:
        imu_directory = os.path.join(directory, 'IMU')
        if not os.path.exists(imu_directory):
            print("IMU directory not found in the specified path.")
            return

        imu_files = [f for f in os.listdir(imu_directory) if f.endswith('.csv')]

        if not imu_files:
            print("No CSV files found in the IMU directory.")
            return

        print("Files available for IMU analysis:")
        for idx, file in enumerate(imu_files):
            print(f"{idx + 1}. {file}")

        file_choice = []
        file_labels = []
        k = 0
        repeat = True

        while repeat:
            choice = int(input("Enter the number corresponding to the file: ")) - 1
            if k >= 1:
                if 0 <= choice < len(imu_files):
                    if choice in file_choice:
                        print("File already selected")
                        if input("Are you done? (y/n)").lower() in yes:
                            repeat = False
                    else: 
                        file_choice.append(choice)
                        label = input(f"Enter a label for {imu_files[choice]}: ")
                        file_labels.append(label)
                        if input("Are you done? (y/n)").lower() in yes:
                            repeat = False
                else:
                    print("Invalid selection. Please choose a valid file number.")
            elif k == 0:
                if 0 <= choice < len(imu_files):
                    file_choice.append(choice)
                    label = input(f"Enter a label for {imu_files[choice]}: ")
                    file_labels.append(label)
                    if input("Are you done? (y/n)").lower() in yes:
                        repeat = False
                        k += 1
                else:
                    print("Invalid selection. Please choose a valid file number.")

        file_path = [os.path.join(imu_directory, imu_files[i]) for i in file_choice]

        imu_choise = input(
            "Enter '1' for Unprocessed data, '2' for Processed data, '3' for Denoised data, or '4' for Peaks: ")
        if imu_choise == '1':
            print("Unprocessed data is being plotted")
            IMU_analysis(file_path, file_labels, 'unprocessed', wavelet_type, level, colors)
        elif imu_choise == '2':
            print("Processed data is being plotted")
            IMU_analysis(file_path, file_labels, 'psd', wavelet_type, level, alt_color)
        elif imu_choise == '3':
            print("Denoised data is being plotted")
            IMU_analysis(file_path, file_labels, 'denoised', wavelet_type, level, colors)
        elif imu_choise == '4':
            print("Peaks being plotted")
            IMU_analysis(file_path, file_labels, 'Peaks', wavelet_type, level, alt_color)

        run_again = input("Run again? (y/n): ").strip().lower()
        if run_again not in yes:
            print("Exiting the program.")
            break



def acoustic(directory):
    print("Welcome to the Acoustic analysis tool.")
    
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
            analysis_choice = input("1. FFT analysis\n2. Raw data analysis\n3. Segmentation analysis\n4. Linear regression\n5. RMS plot\nInput:")

            if analysis_choice == '1':  # FFT analysis
                perform_fft_analysis(subdir_path)
                
            elif analysis_choice == '2':  # Raw data analysis
                plot_raw_data(subdir_path)
                
            elif analysis_choice == '3':  # Segmentation analysis
                segmentation_analysis(subdir_path,window_samples, step_size, sample_rate, sample_dir, output_dir, amp_tol, amp_var_tol)

            elif analysis_choice=='4':    # linear regression
                plot_scatter(subdir_path)  
                
            elif analysis_choice=='5':    # linear regression
                plot_rms(subdir_path)  
                
            else:
                print("Invalid selection. Please choose '1' or '2'.")

        else:
            print("Invalid selection. Please choose a valid subfolder.")
        
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
            IMU(base_directory, wavelet_type, level, colors, alt_color)
        else:
            print("Invalid selection. Please restart and choose '1' or '2'.")
    else:
        print("Invalid selection. Please restart and choose a valid person number.")

if __name__ == "__main__":
    main()
