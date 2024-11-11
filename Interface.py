import os
from AnalysisAcoustic import perform_fft_analysis  # import
from csv_compiler import npz_rm
from csv_compiler import csv_compiler
from IMU import IMU_analysis

# Predefined paths for each person
person_paths = {
    'Ali': r'C:\\Users\\Ali\\OneDrive - Aalborg Universitet\\Desktop\\P7\\Data\\',
    'Sofus': r'C:\\Users\\bemme\\Downloads\\data\\',
    'Dipendra': 'C:\\Users\\Person3\\Downloads\\data\\',
    'Theis': 'C:\\Users\\Person4\\Downloads\\data\\',
    'Zahid': 'C:\\Users\\Person5\\Downloads\\data\\',
}
def IMU(subdirs,directory):
    print("Welcome to IMU analysis tool")
    print("Please select your name from the list")
    IMU_analysis(subdirs,directory)

def acoustic(subdirs, directory):
    print("Welcome to the Acoustic analysis tool.")
    print("Please select your name from the list:")
            
    print("Please select a subfolder:")
    for idx, subdir in enumerate(subdirs):
        print(f"{idx + 1}. {subdir}")

        sub_choice = int(input("Enter the number corresponding to the subfolder: ")) - 1

        if 0 <= sub_choice < len(subdirs):

            selected_subdir = subdirs[sub_choice]
            subdir_path = os.path.join(directory, selected_subdir)
            print(f"You selected {selected_subdir}. Full path: {subdir_path}")
            
            # Ask if conversion is wanted
            yes = {'yes','y', 'Y', 'ye', ''}
            no = {'no','n'}

            convert = input("Would you like to convert the files? (y/n)").lower()
            if convert in yes:
                convert_files = True
            elif convert in no:
                convert_files = False
            else:
                print("Please respond with 'yes' or 'no'")

            # Convert files if selected
            if convert_files == True:
                csv_compiler(subdir_path)

                # Delete npz files after conversion
                npz_rm(subdir_path)
                print("Files converted to CSV and npz files deleted")
            else:
                print("Files already CSV")

            # Perform the FFT analysis on the selected subdirectory
            perform_fft_analysis(subdir_path)
            
        else:
            print("Invalid selection. Please restart and choose a valid subfolder.")
    else:
        print("Invalid selection. Please restart and choose a valid number.")

def main():
    print ("Welcome to data processing")
    print ("Please choose between Acoustic and IMU")
    analysis_choice = input("Enter '1' for Acoustic analysis or '2' for IMU analysis: ")

    persons = list(person_paths.keys())
    for idx, person in enumerate(persons):
        print(f"{idx + 1}. {person}")
    
    # Get user selection
    choice = int(input("Enter the number corresponding to your name: ")) - 1

    if 0 <= choice < len(persons):
        selected_person = persons[choice]
        directory = person_paths[selected_person]
        print(f"You selected {selected_person}. Data directory: {directory}")

        # List subdirectories in the selected path
        subdirs = [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
        
        if not subdirs:
            print("No subdirectories found in the specified directory.")
            return
    # Run the selected analysis function
        if analysis_choice == '1':
            acoustic(subdirs, directory)
        elif analysis_choice == '2':
            IMU(subdirs,directory)
        else:
            print("Invalid selection. Please restart and choose '1' or '2'.")
    else:
        print("Invalid selection. Please restart and choose a valid person number.")
if __name__ == "__main__":
    main()
