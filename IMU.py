import csv
import matplotlib.pyplot as plt
import pywt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks

# Function for IMU csv reader
def IMU_analysis(file_path, file_choice, plot_type, wavelet_type, level, chosen_colors):
    # Initialize lists to store data for each file
    all_x_values = []
    all_y_values = []
    all_z_values = []
    all_time_values = []
    
    for i in range(len(file_choice)):
        # Temporary lists to store data for each file
        x_values_temp = []
        y_values_temp = []
        z_values_temp = []
        time_values_temp = []
        
        try:
            # Open the CSV file and read it using pandas
            df = pd.read_csv(file_path[i])

            # Check if the CSV has enough columns to process
            if len(df.columns) >= 5:
                # Iterate over each row in the DataFrame
                for index, row in df.iterrows():
                    # Use the row index for time (each row is 1/100th of a second)
                    relative_time = index * 0.01  # Time in seconds (1/100th of a second per row)

                    # Collect data for plotting
                    time_values_temp.append(relative_time)  # Use relative time based on row index
                    x_values_temp.append(float(row.iloc[2]))  # Column 2 (X-axis data)
                    y_values_temp.append(float(row.iloc[3]))  # Column 3 (Y-axis data)
                    z_values_temp.append(float(row.iloc[4]))  # Column 4 (Z-axis data)

            # Append the data for each file to the main lists
            all_x_values.append(x_values_temp)
            all_y_values.append(y_values_temp)
            all_z_values.append(z_values_temp)
            all_time_values.append(time_values_temp)  # Ensure this is a list of time values

        except FileNotFoundError:
            print(f"Error: File {file_path[i]} not found.")
        except ValueError as e:
            print(f"Error processing file {file_path[i]}: {e}")

    # Process the data and plot based on the plot_type argument
    if plot_type == 'unprocessed':
        plot_unprocessed_data(file_choice, all_time_values, all_x_values, all_y_values, all_z_values, chosen_colors)
    elif plot_type == 'psd':
        plot_psd_data(file_choice, all_time_values, all_x_values, all_y_values, all_z_values, wavelet_type, level, chosen_colors)
    elif plot_type == 'denoised':
        plot_denoised(file_choice, all_time_values, all_x_values, all_y_values, all_z_values, wavelet_type, level, chosen_colors)
    elif plot_type == 'Peaks':
        peak_find(file_choice, all_time_values, all_x_values, all_y_values, all_z_values, wavelet_type, level, chosen_colors)


# Function to perform wavelet transform and return processed data
def wavelet_transform(data, wavelet, level):
    # Perform Discrete Wavelet Transform (DWT) to filter the data
    coeffs = pywt.wavedec(data, wavelet, level=level)
    
    # Reconstruct the data using the approximation coefficients (low-pass filter)
    reconstructed_data = pywt.waverec([coeffs[0]] + [np.zeros_like(c) for c in coeffs[1:]], wavelet)
    
    # Ensure the reconstructed data has the same length as the input
    return reconstructed_data[:len(data)]


# Function to plot Power Spectral Density (PSD) for each axis after wavelet processing
from matplotlib.ticker import MaxNLocator

def plot_psd_data(file_labels, all_time_values, all_x_values, all_y_values, all_z_values, wavelet_type, level, chosen_colors):
    import matplotlib.ticker as ticker
    
    plt.figure(figsize=(14, 12))
    sampling_freq = 1 / 0.01  # 1/100th of a second

    # Subplot for X data
    plt.subplot(3, 1, 1)
    for i, label in enumerate(file_labels):
        color = next(chosen_colors)
        processed_x = wavelet_transform(all_x_values[i], wavelet_type, level)
        plt.psd(processed_x, Fs=sampling_freq, label=label, color=color)
    plt.title('Power Spectral Density (X)', pad=15)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power/Frequency (dB/Hz)')
    plt.legend()
    plt.grid(True)
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=10))

    # Subplot for Y data
    plt.subplot(3, 1, 2)
    for i, label in enumerate(file_labels):
        color = next(chosen_colors)
        processed_y = wavelet_transform(all_y_values[i], wavelet_type, level)
        plt.psd(processed_y, Fs=sampling_freq, label=label, color=color)
    plt.title('Power Spectral Density (Y)', pad=15)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power/Frequency (dB/Hz)')
    plt.legend()
    plt.grid(True)
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=10))

    # Subplot for Z data
    plt.subplot(3, 1, 3)
    for i, label in enumerate(file_labels):
        color = next(chosen_colors)
        processed_z = wavelet_transform(all_z_values[i], wavelet_type, level)
        plt.psd(processed_z, Fs=sampling_freq, label=label, color=color)
    plt.title('Power Spectral Density (Z)', pad=15)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power/Frequency (dB/Hz)')
    plt.legend()
    plt.grid(True)
    plt.gca().yaxis.set_major_locator(ticker.MaxNLocator(nbins=10))

    plt.tight_layout(pad=3.0)
    plt.show()


# Function to plot unprocessed data (time vs. X, Y, Z)
def plot_unprocessed_data(file_choice, time_values, x_values, y_values, z_values, chosen_colors):
    plt.figure(figsize=(14, 8))

    for i, file_name in enumerate(file_choice):
        color = next(chosen_colors)

        plt.subplot(3, 1, 1)
        plt.plot(time_values[i], x_values[i], label=f'X Values - {file_name}', color=color)
        plt.title('X vs. Time (Unprocessed)')
        plt.xlabel('Time (s)')
        plt.ylabel('X')
        plt.grid(True)  # Add grid

        color = next(chosen_colors)

        plt.subplot(3, 1, 2)
        plt.plot(time_values[i], y_values[i], label=f'Y Values - {file_name}', color=color)
        plt.title('Y vs. Time (Unprocessed)')
        plt.xlabel('Time (s)')
        plt.ylabel('Y')
        plt.grid(True)  # Add grid

        color = next(chosen_colors)

        plt.subplot(3, 1, 3)
        plt.plot(time_values[i], z_values[i], label=f'Z Values - {file_name}', color=color)
        plt.title('Z vs. Time (Unprocessed)')
        plt.xlabel('Time (s)')
        plt.ylabel('Z')
        plt.grid(True)  # Add grid

    plt.tight_layout()  # Adjusts spacing to prevent overlap
    plt.show()


# Function to plot denoised data after wavelet processing
def plot_denoised(file_choice, time_values, all_x_values, all_y_values, all_z_values, wavelet_type, level, chosen_colors):
    plt.figure(figsize=(14, 8))

    for i, file_name in enumerate(file_choice):

        # Get the next color from the cycle
        color = next(chosen_colors)

        processed_x = wavelet_transform(all_x_values[i], wavelet_type, level)
        plt.subplot(3, 1, 1)
        plt.plot(time_values[i], processed_x, label=f'X Values - {file_name}', color=color)
        plt.title('X vs. Time (Denoised)')
        plt.xlabel('Time (s)')
        plt.ylabel('X')
        plt.grid(True)  # Add grid

        color = next(chosen_colors)

        plt.subplot(3, 1, 2)
        processed_y = wavelet_transform(all_y_values[i], wavelet_type, level)
        plt.plot(time_values[i], processed_y, label=f'Y Values - {file_name}', color=color)
        plt.title('Y vs. Time (Denoised)')
        plt.xlabel('Time (s)')
        plt.ylabel('Y')
        plt.grid(True)  # Add grid

        color = next(chosen_colors)

        plt.subplot(3, 1, 3)
        processed_z = wavelet_transform(all_z_values[i], wavelet_type, level)
        plt.plot(time_values[i], processed_z, label=f'Z Values - {file_name}', color=color)
        plt.title('Z vs. Time (Denoised)')
        plt.xlabel('Time (s)')
        plt.ylabel('Z')
        plt.grid(True)  # Add grid

    plt.tight_layout()  # Adjusts spacing to prevent overlap
    plt.show()


# Function to find and plot peaks
def peak_find(file_choice, time_values, all_x_values, all_y_values, all_z_values, wavelet_type, level, chosen_colors):
    plt.figure(figsize=(14, 8))

    for i, file_name in enumerate(file_choice):
        # Process the data using wavelet transform
        processed_x = wavelet_transform(all_x_values[i], wavelet_type, level)

        # Ensure time_values[i] is a numpy array for proper indexing
        time_values_np = np.array(time_values[i])

        # Find peaks in the processed X data
        peaks_x, _ = find_peaks(processed_x)

        color = next(chosen_colors)
        plt.subplot(3, 1, 1)
        plt.plot(time_values_np, processed_x, label=f'X Values - {file_name}', color=color)

        # Scatter peaks on the plot
        plt.scatter(time_values_np[peaks_x], processed_x[peaks_x], color='red', marker='x', label='Peaks')
        plt.title('X vs. Time (Peaks)')
        plt.xlabel('Time (s)')
        plt.ylabel('X')
        plt.legend()
        plt.grid(True)  # Add grid

        # Process Y data
        processed_y = wavelet_transform(all_y_values[i], wavelet_type, level)
        peaks_y, _ = find_peaks(processed_y)

        color = next(chosen_colors)
        plt.subplot(3, 1, 2)
        plt.plot(time_values_np, processed_y, label=f'Y Values - {file_name}', color=color)
        plt.scatter(time_values_np[peaks_y], processed_y[peaks_y], color='red', marker='x', label='Peaks')
        plt.title('Y vs. Time (Peaks)')
        plt.xlabel('Time (s)')
        plt.ylabel('Y')
        plt.legend()
        plt.grid(True)  # Add grid

        # Process Z data
        processed_z = wavelet_transform(all_z_values[i], wavelet_type, level)
        peaks_z, _ = find_peaks(processed_z)

        color = next(chosen_colors)
        plt.subplot(3, 1, 3)
        plt.plot(time_values_np, processed_z, label=f'Z Values - {file_name}', color=color)
        plt.scatter(time_values_np[peaks_z], processed_z[peaks_z], color='red', marker='x', label='Peaks')
        plt.title('Z vs. Time (Peaks)')
        plt.xlabel('Time (s)')
        plt.ylabel('Z')
        plt.legend()
        plt.grid(True)  # Add grid

    plt.tight_layout()  # Adjusts spacing to prevent overlap
    plt.show()
