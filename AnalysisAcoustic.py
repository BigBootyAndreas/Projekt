import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

# Function to plot raw mean data (before FFT)
def plot_raw_data(directory):
    # Get all CSV files in the directory
    csv_files = glob.glob(os.path.join(directory, '*.csv'))

    # Initialize lists to store time and Column 3 data from all files
    col3_all = []
    time_all = []

    # Process each CSV file and collect time and Column 3 data
    for file_path in csv_files:
        print(f'Processing file: {file_path}')
        
        # Read CSV and extract columns
        data = pd.read_csv(file_path)
        time = data.iloc[:, 1].values  # Assuming column 2 is the time
        col3 = data.iloc[:, 2].values  # Column 3

        if len(col3) == 0 or len(time) == 0:
            print(f"Warning: {file_path} contains no data in Column 2 or 3.")
            continue
        
        # Append to the lists
        time_all.append(time)
        col3_all.append(col3)

    if not col3_all:
        print("No valid data found in Column 2 or 3 of any CSV file.")
        return

    # Ensure all collected data is of the same length
    min_length = min(map(len, col3_all))
    col3_all = [col[:min_length] for col in col3_all]
    time_all = [t[:min_length] for t in time_all]

    # Compute the mean
    mean_col3 = np.mean(col3_all, axis=0)
    mean_time = np.mean(time_all, axis=0)  # Average time axis

    # Plot the raw mean data
    plt.figure(figsize=(12, 6))
    plt.plot(mean_time, mean_col3, label='Mean Column 3 (Raw Data)', color='b')
    plt.title('Raw Data: Mean Column 3 vs Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    plt.legend()
    plt.show()

# Existing function for FFT analysis (already provided)
def perform_fft_analysis(directory):
    # Get all CSV files in the directory
    csv_files = glob.glob(os.path.join(directory, '*.csv'))

    # Initialize lists to store time and Column 3 data from all files
    col3_all = []
    time_all = []

    # Process each CSV file and collect time and Column 3 data
    for file_path in csv_files:
        print(f'Processing file: {file_path}')
        
        # Read CSV and extract columns
        data = pd.read_csv(file_path)
        time = data.iloc[:, 1].values  # Assuming column 2 is the time
        col3 = data.iloc[:, 2].values  # Column 3

        if len(col3) == 0 or len(time) == 0:
            print(f"Warning: {file_path} contains no data in Column 2 or 3.")
            continue
        
        # Append to the lists
        time_all.append(time)
        col3_all.append(col3)

    if not col3_all:
        print("No valid data found in Column 2 or 3 of any CSV file.")
        return

    # Ensure all collected data is of the same length
    min_length = min(map(len, col3_all))
    col3_all = [col[:min_length] for col in col3_all]
    time_all = [t[:min_length] for t in time_all]

    # Compute the mean
    mean_col3 = np.mean(col3_all, axis=0)
    mean_time = np.mean(time_all, axis=0)  # Average time axis

    # Normalize the mean data
    mean_col3 = mean_col3 / np.max(np.abs(mean_col3))

    # Perform FFT on the mean Column 3
    fft_mean_col3 = np.fft.fft(mean_col3)

    # Compute the frequency axis
    n = len(mean_col3)
    freq = np.fft.fftfreq(n, d=(mean_time[1] - mean_time[0]))  # Use actual time intervals

    # Create a figure with two subplots: one for FFT and one for the spectrogram
    fig, ax = plt.subplots(2, 1, figsize=(12, 10))

    # Plot the FFT results
    ax[0].plot(freq[:n//2], np.abs(fft_mean_col3)[:n//2])  # Take positive frequencies only
    ax[0].set_title('FFT of Mean Acoustic Data')
    ax[0].set_xlabel('Frequency (Hz)')
    ax[0].set_ylabel('Magnitude')
    ax[0].grid(True)

    # Plot the spectrogram of the mean data with time as the x-axis
    ax[1].specgram(mean_col3, NFFT=256, Fs=1.0 / (mean_time[1] - mean_time[0]), noverlap=128, cmap='plasma')
    ax[1].set_title('Spectrogram of Mean Acoustic Data')
    ax[1].set_xlabel('Time (s)')
    ax[1].set_ylabel('Frequency (Hz)')
    ax[1].grid(True)

    # Adjust layout for better visualization    
    plt.tight_layout()
    plt.show()