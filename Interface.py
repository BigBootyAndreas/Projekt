import os
from AnalysisAcoustic import perform_fft_analysis  # import

# Predefined paths for each person
person_paths = {
    'Ali': r'C:\\Users\\Ali\\OneDrive - Aalborg Universitet\\Desktop\\P7\\Data\\',
    'Sofus': 'C:\\Users\\Person2\\Downloads\\data\\',
    'Dipendra': 'C:\\Users\\Person3\\Downloads\\data\\',
    'Theis': 'C:\\Users\\Person4\\Downloads\\data\\',
    'Zahid': 'C:\\Users\\Person5\\Downloads\\data\\',
}

def main():
    print("Welcome to the FFT Analysis Tool.")
    print("Please select your name from the list:")
    
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
        
        print("Please select a subfolder:")
        for idx, subdir in enumerate(subdirs):
            print(f"{idx + 1}. {subdir}")

        sub_choice = int(input("Enter the number corresponding to the subfolder: ")) - 1

        if 0 <= sub_choice < len(subdirs):
            selected_subdir = subdirs[sub_choice]
            subdir_path = os.path.join(directory, selected_subdir)
            print(f"You selected {selected_subdir}. Full path: {subdir_path}")

            # Perform the FFT analysis on the selected subdirectory
            perform_fft_analysis(subdir_path)
        else:
            print("Invalid selection. Please restart and choose a valid subfolder.")
    else:
        print("Invalid selection. Please restart and choose a valid number.")

if __name__ == "__main__":
    main()