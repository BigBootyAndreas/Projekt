import csv
import matplotlib.pyplot as plt
import pywt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks, welch

# Function for IMU csv reader
def IMU_analysis(file_path, file_choice, plot_type, wavelet_type, level, chosen_colors):
    all_x_values = []
    all_y_values = []
    all_z_values = []
    all_time_values = []
    
    for i in range(len(file_choice)):
        x_values_temp = []
        y_values_temp = []
        z_values_temp = []
        time_values_temp = []
        
        try:
            df = pd.read_csv(file_path[i])
            if len(df.columns) >= 5:
                for index, row in df.iterrows():
                    relative_time = index * 0.01  # Time in seconds (1/100th of a second per row)
                    time_values_temp.append(relative_time)
                    x_values_temp.append(float(row.iloc[1]))
                    y_values_temp.append(float(row.iloc[2]))
                    z_values_temp.append(float(row.iloc[3]))

            all_x_values.append(x_values_temp)
            all_y_values.append(y_values_temp)
            all_z_values.append(z_values_temp)
            all_time_values.append(time_values_temp)

        except FileNotFoundError:
            print(f"Error: File {file_path[i]} not found.")
        except ValueError as e:
            print(f"Error processing file {file_path[i]}: {e}")

    if plot_type == 'unprocessed':
        plot_unprocessed_data(file_choice, all_time_values, all_x_values, all_y_values, all_z_values, chosen_colors)
    elif plot_type == 'psd':
        plot_psd_data(file_choice, all_time_values, all_x_values, all_y_values, all_z_values, wavelet_type, level, chosen_colors)
    elif plot_type == 'denoised':
        plot_denoised(file_choice, all_time_values, all_x_values, all_y_values, all_z_values, wavelet_type, level, chosen_colors)
    elif plot_type == 'Peaks':
        peak_find(file_choice, all_time_values, all_x_values, all_y_values, all_z_values, wavelet_type, level, chosen_colors)


# Updated Wavelet Transform Function
def wavelet_transform(data, wavelet, level):
    coeffs = pywt.wavedec(data, wavelet, level=level)
    reconstructed_data = pywt.waverec(coeffs, wavelet)  # Use all coefficients for reconstruction
    return reconstructed_data[:len(data)]


# Updated PSD Plot Function with Welch's Method and Logarithmic Safety
def plot_psd_data(file_labels, all_time_values, all_x_values, all_y_values, all_z_values, wavelet_type, level, chosen_colors):
    plt.figure(figsize=(14, 12))
    
    for i, label in enumerate(file_labels):
        sampling_freq = 1 / np.mean(np.diff(all_time_values[i]))  # Dynamically calculate sampling frequency

        color = next(chosen_colors)

        # Process and plot X data
        processed_x = wavelet_transform(all_x_values[i], wavelet_type, level)
        f, psd = welch(processed_x, fs=sampling_freq, nperseg=256)
        psd_safe = np.maximum(psd, 1e-10)  # Avoid log(0)
        plt.subplot(3, 1, 1)
        plt.semilogy(f, psd_safe, label=label, color=color)
        plt.title('Power Spectral Density (X)', pad=15)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power/Frequency (dB/Hz)')
        plt.legend()
        plt.grid(True)

        # Process and plot Y data
        processed_y = wavelet_transform(all_y_values[i], wavelet_type, level)
        f, psd = welch(processed_y, fs=sampling_freq, nperseg=256)
        psd_safe = np.maximum(psd, 1e-10)  # Avoid log(0)
        plt.subplot(3, 1, 2)
        plt.semilogy(f, psd_safe, label=label, color=color)
        plt.title('Power Spectral Density (Y)', pad=15)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power/Frequency (dB/Hz)')
        plt.legend()
        plt.grid(True)

        # Process and plot Z data
        processed_z = wavelet_transform(all_z_values[i], wavelet_type, level)
        f, psd = welch(processed_z, fs=sampling_freq, nperseg=256)
        psd_safe = np.maximum(psd, 1e-10)  # Avoid log(0)
        plt.subplot(3, 1, 3)
        plt.semilogy(f, psd_safe, label=label, color=color)
        plt.title('Power Spectral Density (Z)', pad=15)
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Power/Frequency (dB/Hz)')
        plt.legend()
        plt.grid(True)

    plt.tight_layout(pad=3.0)
    plt.show()


# Remaining Functions (No Changes Required)
def plot_unprocessed_data(file_choice, time_values, x_values, y_values, z_values, chosen_colors):
    plt.figure(figsize=(14, 8))
    for i, file_name in enumerate(file_choice):
        color = next(chosen_colors)
        plt.subplot(3, 1, 1)
        plt.plot(time_values[i], x_values[i], label=f'X Values - {file_name}', color=color)
        plt.title('X vs. Time (Unprocessed)')
        plt.xlabel('Time (s)')
        plt.ylabel('X')
        plt.grid(True)

        color = next(chosen_colors)
        plt.subplot(3, 1, 2)
        plt.plot(time_values[i], y_values[i], label=f'Y Values - {file_name}', color=color)
        plt.title('Y vs. Time (Unprocessed)')
        plt.xlabel('Time (s)')
        plt.ylabel('Y')
        plt.grid(True)

        color = next(chosen_colors)
        plt.subplot(3, 1, 3)
        plt.plot(time_values[i], z_values[i], label=f'Z Values - {file_name}', color=color)
        plt.title('Z vs. Time (Unprocessed)')
        plt.xlabel('Time (s)')
        plt.ylabel('Z')
        plt.grid(True)

    plt.tight_layout()
    plt.show()


def plot_denoised(file_choice, time_values, all_x_values, all_y_values, all_z_values, wavelet_type, level, chosen_colors):
    plt.figure(figsize=(14, 8))
    for i, file_name in enumerate(file_choice):
        color = next(chosen_colors)
        processed_x = wavelet_transform(all_x_values[i], wavelet_type, level)
        plt.subplot(3, 1, 1)
        plt.plot(time_values[i], processed_x, label=f'X Values - {file_name}', color=color)
        plt.title('X vs. Time (Denoised)')
        plt.xlabel('Time (s)')
        plt.ylabel('X')
        plt.grid(True)

        color = next(chosen_colors)
        processed_y = wavelet_transform(all_y_values[i], wavelet_type, level)
        plt.subplot(3, 1, 2)
        plt.plot(time_values[i], processed_y, label=f'Y Values - {file_name}', color=color)
        plt.title('Y vs. Time (Denoised)')
        plt.xlabel('Time (s)')
        plt.ylabel('Y')
        plt.grid(True)

        color = next(chosen_colors)
        processed_z = wavelet_transform(all_z_values[i], wavelet_type, level)
        plt.subplot(3, 1, 3)
        plt.plot(time_values[i], processed_z, label=f'Z Values - {file_name}', color=color)
        plt.title('Z vs. Time (Denoised)')
        plt.xlabel('Time (s)')
        plt.ylabel('Z')
        plt.grid(True)

    plt.tight_layout()
    plt.show()

# Function to find and plot peaks
def peak_find(file_choice, time_values, all_x_values, all_y_values, all_z_values, wavelet_type, level, chosen_colors):
    plt.figure(figsize=(14, 8))

    for i, file_name in enumerate(file_choice):
        # Ensure time_values[i] is a numpy array for proper indexing
        time_values_np = np.array(time_values[i])

        # Process the X data
        processed_x = wavelet_transform(all_x_values[i], wavelet_type, level)
        peaks_x, _ = find_peaks(processed_x, height=None, distance=10)  # Modify distance as needed

        color = next(chosen_colors)
        plt.subplot(3, 1, 1)
        plt.plot(time_values_np, processed_x, label=f'X Values - {file_name}', color=color)
        plt.scatter(time_values_np[peaks_x], processed_x[peaks_x], color='red', marker='x', label='Peaks')
        plt.title('X vs. Time (Peaks)')
        plt.xlabel('Time (s)')
        plt.ylabel('X')
        plt.legend()
        plt.grid(True)

        # Process the Y data
        processed_y = wavelet_transform(all_y_values[i], wavelet_type, level)
        peaks_y, _ = find_peaks(processed_y, height=None, distance=10)  # Modify distance as needed

        color = next(chosen_colors)
        plt.subplot(3, 1, 2)
        plt.plot(time_values_np, processed_y, label=f'Y Values - {file_name}', color=color)
        plt.scatter(time_values_np[peaks_y], processed_y[peaks_y], color='red', marker='x', label='Peaks')
        plt.title('Y vs. Time (Peaks)')
        plt.xlabel('Time (s)')
        plt.ylabel('Y')
        plt.legend()
        plt.grid(True)

        # Process the Z data
        processed_z = wavelet_transform(all_z_values[i], wavelet_type, level)
        peaks_z, _ = find_peaks(processed_z, height=None, distance=10)  # Modify distance as needed

        color = next(chosen_colors)
        plt.subplot(3, 1, 3)
        plt.plot(time_values_np, processed_z, label=f'Z Values - {file_name}', color=color)
        plt.scatter(time_values_np[peaks_z], processed_z[peaks_z], color='red', marker='x', label='Peaks')
        plt.title('Z vs. Time (Peaks)')
        plt.xlabel('Time (s)')
        plt.ylabel('Z')
        plt.legend()
        plt.grid(True)

    plt.tight_layout()
    plt.show()
