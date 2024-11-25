import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import seaborn as sns

# Function to calculate mean and RMS of Column 3 in each file
def calculate_means_and_rms(directory):
    # Get all CSV files in the directory
    csv_files = glob.glob(os.path.join(directory, '*.csv'))
    print(f"Found {len(csv_files)} CSV files in the directory.")

    # Lists to store file names, mean values, and RMS values
    file_names = []
    mean_values = []
    rms_values = []

    for file_path in csv_files:
        print(f'Processing file: {file_path}')
        
        try:
            # Read the CSV file
            data = pd.read_csv(file_path)
            print(f"Data shape: {data.shape}")

            # Check if the file has at least 3 columns
            if data.shape[1] < 3:
                print(f"Warning: {file_path} does not have enough columns.")
                continue

            # Extract Column 3
            col3 = data.iloc[:, 2].values  # Assuming Column 3 contains amplitude data
            if len(col3) == 0:
                print(f"Warning: {file_path} contains no data in Column 3.")
                continue

            # Compute the mean of Column 3
            col3_mean = np.mean(col3)
            print(f"Mean value for {file_path}: {col3_mean}")

            # Compute the RMS of Column 3
            col3_rms = np.sqrt(np.mean(col3**2))
            print(f"RMS value for {file_path}: {col3_rms}")

            # Store the file name, mean, and RMS values
            file_names.append(os.path.basename(file_path))  # Use only file name for labeling
            mean_values.append(col3_mean)
            rms_values.append(col3_rms)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            continue

    return file_names, mean_values, rms_values


# Function to create scatter plots of mean and RMS values
def plot_rms(directory):
    # Calculate means and RMS for all files
    file_names, _, rms_values = calculate_means_and_rms(directory)

    if not rms_values:
        print("No RMS values found for plotting.")
        return

    # Create a distribution plot for RMS values
    plt.figure(figsize=(10, 6))

    # Plot histogram and KDE
    sns.histplot(rms_values, kde=True, color='green', bins=20, alpha=0.7)  # Histogram with KDE overlay

    plt.title('RMS Amplitude Distribution of Acoustic Data')
    plt.xlabel('RMS Amplitude')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.tight_layout()
    plt.show()


# Main function for standalone script
if __name__ == "__main__":
    # Example of how this script is linked with the second script:
    # The directory is passed dynamically by the second script
    directory = input("Enter the directory containing the CSV files: ").strip()
    
    # Plot the scatter plots for mean and RMS
    plot_rms(directory)
