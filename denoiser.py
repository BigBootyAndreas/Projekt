import os
import pandas as pd
import numpy as np
import pywt

# Wavelet denoising function
def wavelet_denoise(data, wavelet='db1', level=5, thresholding='soft'):
    # Perform wavelet decomposition
    coeffs = pywt.wavedec(data, wavelet, level=level)
    
    # Calculate threshold for noise removal
    threshold = np.median(np.abs(coeffs[-1])) / 0.6745 * np.sqrt(2 * np.log(len(data)))
    
    # Apply thresholding to detail coefficients
    coeffs_denoised = [coeffs[0]] + [pywt.threshold(c, threshold, mode=thresholding) for c in coeffs[1:]]
    
    # Reconstruct the signal from the denoised coefficients
    denoised_data = pywt.waverec(coeffs_denoised, wavelet)
    
    # Ensure the reconstructed data length matches the original
    return denoised_data[:len(data)]

def csv_rm(folder_path):

    files = os.listdir(folder_path)

    # Filter out only the .npz files
    npz_files = [file for file in files if file.endswith(".csv")]

    # Convert the .npz files to .csv files, saving the timestamp in the first column,
    # the time in the second column, and the amplitude in the third
    for filename in npz_files:
        full_path = os.path.join(folder_path, filename)
        
        # Remove the .npz file
        os.remove(full_path)
        print(f"Deleted {filename}")

# Denoising CSV files
def denoise_csv_files(input_dir, output_dir, column_to_denoise=None, wavelet='db1', level=5, thresholding='soft'):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".csv"):
            filepath = os.path.join(input_dir, filename)
            output_filepath = os.path.join(output_dir, f"denoised_{filename}")

            # Load CSV file
            df = pd.read_csv(filepath)

            # Denoise specific column or all columns
            if column_to_denoise:
                if column_to_denoise in df.columns:
                    df[column_to_denoise] = wavelet_denoise(df[column_to_denoise].values, wavelet, level, thresholding)
                else:
                    print(f"Column '{column_to_denoise}' not found in {filename}. Skipping file.")
                    continue
            else:
                for col in df.select_dtypes(include=[np.number]).columns:
                    df[col] = wavelet_denoise(df[col].values, wavelet, level, thresholding)

            # Save the denoised data
            df.to_csv(output_filepath, index=False)
            print(f"Denoised file saved: {output_filepath}")

# Specify directories and parameters
input_directory = r'C:\\Users\\bemme\\Downloads\\data\\Acoustic\\emill'
output_directory = r'C:\\Users\\bemme\\Downloads\\data\\Acoustic\\emill'
column_name_to_denoise = None  # Set to specific column name or None for all numerical columns

def main():
    # Run the script
    denoise_csv_files(
        input_dir=input_directory,
        output_dir=output_directory,
        column_to_denoise=column_name_to_denoise,
        wavelet='db1',
        level=5,
        thresholding='soft'
    )

if __name__ == "__main__":
    main()
