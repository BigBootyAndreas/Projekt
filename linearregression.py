import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

# Function to calculate mean of Column 3 in each file
def calculate_means(directory):
    # Get all CSV files in the directory
    csv_files = glob.glob(os.path.join(directory, '*.csv'))
    print(f"Found {len(csv_files)} CSV files in the directory.")

    # Lists to store file names and their mean values
    file_names = []
    mean_values = []

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

            # Store the file name and its mean value
            file_names.append(os.path.basename(file_path))  # Use only file name for labeling
            mean_values.append(col3_mean)

        except Exception as e:
            print(f"Error processing file {file_path}: {e}")
            continue

    return file_names, mean_values

# Function to create a scatter plot of mean values
def plot_scatter(directory):
    # Calculate means for all files
    file_names, mean_values = calculate_means(directory)

    if not mean_values:
        print("No valid mean values found.")
        return

    # Create scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(file_names, mean_values, color='blue', s=100, alpha=0.7)
    plt.title('Mean Amplitude of Acoustic Data for Each File')
    plt.xlabel('File Name')
    plt.ylabel('Mean Amplitude')
    plt.xticks(rotation=45, ha='right')
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Main function for standalone script
if __name__ == "__main__":
    # Example of how this script is linked with the second script:
    # The directory is passed dynamically by the second script
    directory = input("Enter the directory containing the CSV files: ").strip()
    
    # Plot the scatter plot
    plot_scatter(directory)
