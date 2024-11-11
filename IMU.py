import csv
import matplotlib.pyplot as plt
import pywt  # For wavelet transformation
import numpy as np

# Initialize lists to store data for plotting
x_values = []
y_values = []
z_values = []
time_values = []

# Function to read and parse the CSV file and process data
def IMU_analysis(subdirs, file_path, plot_type='psd'):
    global x_values, y_values, z_values, time_values
    try:
        with open(file_path, 'r') as csv_file:
            reader = csv.reader(csv_file)
            header = next(reader)  # Skip the header if present

            # Reading data from the CSV file
            for row in reader:
                if len(row) >= 5:  # Ensure the row has at least 5 columns
                    epoch_value = row[4]  # 5th column (epoch in milliseconds)
                    
                    try:
                        # Convert epoch to seconds by dividing by 1000
                        epoch_in_seconds = float(epoch_value) / 1000
                        
                        # Collect data for plotting
                        time_values.append(epoch_in_seconds)
                        x_values.append(float(row[1]))  # Column 2 (X-axis data)
                        y_values.append(float(row[2]))  # Column 3 (Y-axis data)
                        z_values.append(float(row[3]))  # Column 4 (Z-axis data)
                        
                    except ValueError:
                        print(f"Invalid epoch value: {epoch_value}")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")

    # Now, process the data and plot based on the plot_type argument

    if plot_type == 'unprocessed':
        plot_unprocessed_data()
    elif plot_type == 'psd':
        plot_psd_data()

# Function to perform wavelet transform and return processed data
def wavelet_transform(data, wavelet='db4', level=4):
    # Perform Discrete Wavelet Transform (DWT) to filter the data
    coeffs = pywt.wavedec(data, wavelet, level=level)
    
    # Reconstruct the data using the approximation coefficients (low-pass filter)
    reconstructed_data = pywt.waverec([coeffs[0]] + [np.zeros_like(c) for c in coeffs[1:]], wavelet)
    
    return reconstructed_data

# Function to plot unprocessed data (time series data)
def plot_unprocessed_data():
    plt.figure(figsize=(14, 8))

    # Plot for x vs. time (Unprocessed)
    plt.subplot(3, 1, 1)
    plt.plot(time_values, x_values, label='X Values', color='r')
    plt.title('X vs. Time (Unprocessed)')
    plt.xlabel('Time (s)')
    plt.ylabel('X')

    # Plot for y vs. time (Unprocessed)
    plt.subplot(3, 1, 2)
    plt.plot(time_values, y_values, label='Y Values', color='g')
    plt.title('Y vs. Time (Unprocessed)')
    plt.xlabel('Time (s)')
    plt.ylabel('Y')

    # Plot for z vs. time (Unprocessed)
    plt.subplot(3, 1, 3)
    plt.plot(time_values, z_values, label='Z Values', color='b')
    plt.title('Z vs. Time (Unprocessed)')
    plt.xlabel('Time (s)')
    plt.ylabel('Z')

    plt.tight_layout()  # Adjusts spacing to prevent overlap
    plt.show()

# Function to plot Power Spectral Density (PSD) for each axis after wavelet processing
def plot_psd_data():
    plt.figure(figsize=(14, 8))

    # Perform wavelet transform on the data
    processed_x = wavelet_transform(x_values)
    processed_y = wavelet_transform(y_values)
    processed_z = wavelet_transform(z_values)

    # Plot PSD for processed x data
    plt.subplot(3, 1, 1)
    plt.psd(processed_x, Fs=1/(time_values[1] - time_values[0]), color='r')
    plt.title('Power Spectral Density (X) after Wavelet Processing')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power/Frequency (dB/Hz)')

    # Plot PSD for processed y data
    plt.subplot(3, 1, 2)
    plt.psd(processed_y, Fs=1/(time_values[1] - time_values[0]), color='g')
    plt.title('Power Spectral Density (Y) after Wavelet Processing')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power/Frequency (dB/Hz)')

    # Plot PSD for processed z data
    plt.subplot(3, 1, 3)
    plt.psd(processed_z, Fs=1/(time_values[1] - time_values[0]), color='b')
    plt.title('Power Spectral Density (Z) after Wavelet Processing')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power/Frequency (dB/Hz)')

    plt.tight_layout()  # Adjusts spacing to prevent overlap
    plt.show()

# Example usage:
# 1. If you want to see unprocessed data:
# IMU_analysis([], 'path_to_your_csv_file.csv', plot_type='unprocessed')

# 2. If you want to see PSD of processed data:
# IMU_analysis([], 'path_to_your_csv_file.csv', plot_type='psd')
