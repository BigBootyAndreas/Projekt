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
                # Get the starting epoch time for normalization (relative time)
                start_epoch = float(df.iloc[0, 4]) / 1000  # Convert to seconds
                
                # Iterate over each row in the DataFrame
                for _, row in df.iterrows():
                    epoch_value = row.iloc[4]  # Use .iloc for position-based access
                    
                    try:
                        # Convert epoch to seconds by dividing by 1000
                        epoch_in_seconds = float(epoch_value) / 1000
                        # Normalize epoch time to start from 0
                        relative_time = epoch_in_seconds - start_epoch
                        #print(relative_time)
                        # Collect data for plotting
                        time_values_temp.append(relative_time)  # Use relative time
                        x_values_temp.append(float(row.iloc[1]))  # Column 2 (X-axis data)
                        y_values_temp.append(float(row.iloc[2]))  # Column 3 (Y-axis data)
                        z_values_temp.append(float(row.iloc[3]))  # Column 4 (Z-axis data)

                    except ValueError:
                        print(f"Invalid epoch value: {epoch_value}")
            
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
    elif plot_type== 'denoised':
        plot_denoised(file_choice, all_time_values,all_x_values,all_y_values,all_z_values, wavelet_type, level, chosen_colors)
    elif plot_type=='Peaks':
        peak_find(file_choice, all_time_values, all_x_values, all_y_values ,all_z_values, wavelet_type, level, chosen_colors)


# Function to perform wavelet transform and return processed data
def wavelet_transform(data, wavelet, level):
    # Perform Discrete Wavelet Transform (DWT) to filter the data
    coeffs = pywt.wavedec(data, wavelet, level=level)
    
    # Reconstruct the data using the approximation coefficients (low-pass filter)
    reconstructed_data = pywt.waverec([coeffs[0]] + [np.zeros_like(c) for c in coeffs[1:]], wavelet)
    
    # Ensure the reconstructed data has the same length as the input
    return reconstructed_data[:len(data)]

# Function to plot Power Spectral Density (PSD) for each axis after wavelet processing
def plot_psd_data(file_choices, all_time_values, all_x_values, all_y_values, all_z_values, wavelet_type, level, chosen_colors):

    plt.figure(figsize=(14, 12))  # Create a figure large enough for 3 subplots
    
        # Calculate the sampling frequency from the first file (assuming all files have the same time spacing)
    sampling_freq = 1 / (all_time_values[0][1] - all_time_values[0][0])  # this should work now

    # Subplot for X data
    plt.subplot(3, 1, 1)
    for i in range(len(file_choices)):  # Loop over each file's data
        color = next(chosen_colors)
        processed_x = wavelet_transform(all_x_values[i], wavelet_type, level)  # Process the X data using wavelet transform
        plt.psd(processed_x, Fs=sampling_freq, label=f'File {file_choices[i]}', color=color)
    plt.title('Power Spectral Density (X) after Wavelet Processing')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power/Frequency (dB/Hz)')
    plt.legend()

    # Subplot for Y data
    plt.subplot(3, 1, 2)
    for i in range(len(file_choices)):  # Loop over each file's data
        color = next(chosen_colors)
        processed_y = wavelet_transform(all_y_values[i], wavelet_type, level)  # Process the Y data using wavelet transform
        plt.psd(processed_y, Fs=sampling_freq, label=f'File {file_choices[i]}', color=color)
    plt.title('Power Spectral Density (Y) after Wavelet Processing')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power/Frequency (dB/Hz)')
    plt.legend()

    # Subplot for Z data
    plt.subplot(3, 1, 3)
    for i in range(len(file_choices)):  # Loop over each file's data
        color = next(chosen_colors)
        processed_z = wavelet_transform(all_z_values[i], wavelet_type, level)  # Process the Z data using wavelet transform
        plt.psd(processed_z, Fs=sampling_freq, label=f'File {file_choices[i]}', color=color)
    plt.title('Power Spectral Density (Z) after Wavelet Processing')
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Power/Frequency (dB/Hz)')
    plt.legend()

    plt.tight_layout()  # Adjusts spacing to prevent overlap between subplots
    plt.show()

def plot_unprocessed_data(file_choice, time_values, x_values, y_values, z_values, chosen_colors):
    
    plt.figure(figsize=(14, 8))

    for i, file_name in enumerate(file_choice):

        color = next(chosen_colors)

        plt.subplot(3, 1, 1)
        plt.plot(time_values[i], x_values[i], label=f'X Values - {file_name}', color=color)
        plt.title('X vs. Time (Unprocessed)')
        plt.xlabel('Time (s)')
        plt.ylabel('X')

        color = next(chosen_colors)

        plt.subplot(3, 1, 2)
        plt.plot(time_values[i], y_values[i], label=f'Y Values - {file_name}', color=color)
        plt.title('Y vs. Time (Unprocessed)')
        plt.xlabel('Time (s)')
        plt.ylabel('Y')

        color = next(chosen_colors)

        plt.subplot(3, 1, 3)
        plt.plot(time_values[i], z_values[i], label=f'Z Values - {file_name}', color=color)
        plt.title('Z vs. Time (Unprocessed)')
        plt.xlabel('Time (s)')
        plt.ylabel('Z')

    plt.tight_layout()  # Adjusts spacing to prevent overlap
    plt.show()

def plot_denoised(file_choice, time_values, all_x_values, all_y_values ,all_z_values, wavelet_type, level, chosen_colors):

    plt.figure(figsize=(14, 8))

    for i, file_name in enumerate(file_choice):

        # Get the next color from the cycle
        color = next(chosen_colors)

        processed_x = wavelet_transform(all_x_values[i], wavelet_type, level)
        plt.subplot(3, 1, 1)
        plt.plot(time_values[i], processed_x, label=f'X Values - {file_name}', color=color)
        plt.title('X vs. Time (denoising)')
        plt.xlabel('Time (s)')
        plt.ylabel('X')

        color = next(chosen_colors)

        plt.subplot(3, 1, 2)
        processed_y = wavelet_transform(all_y_values[i], wavelet_type, level)
        plt.plot(time_values[i], processed_y, label=f'Y Values - {file_name}', color=color)
        plt.title('Y vs. Time (donoising)')
        plt.xlabel('Time (s)')
        plt.ylabel('Y')

        color = next(chosen_colors)

        plt.subplot(3, 1, 3)
        processed_z = wavelet_transform(all_z_values[i], wavelet_type, level)
        plt.plot(time_values[i], processed_z, label=f'Z Values - {file_name}', color=color)
        plt.title('Z vs. Time (denoising )')
        plt.xlabel('Time (s)')
        plt.ylabel('Z')

    plt.tight_layout()  # Adjusts spacing to prevent overlap
    plt.show()

def peak_find(file_choice, time_values, all_x_values, all_y_values, all_z_values, wavelet_type, level, chosen_colors):
    plt.figure(figsize=(14, 12))
    
    for axis, all_values, axis_label in zip(
        ['X', 'Y', 'Z'], 
        [all_x_values, all_y_values, all_z_values], 
        ['X-axis', 'Y-axis', 'Z-axis']
    ):
        plt.subplot(3, 1, ['X', 'Y', 'Z'].index(axis) + 1)
        for i, file_name in enumerate(file_choice):
            # Apply wavelet transform to denoise the signal
            processed_data = wavelet_transform(all_values[i], wavelet_type, level)
            time = time_values[i]
            
            # Find peaks
            peaks, _ = find_peaks(processed_data, height=None)  
            
            if len(peaks) > 0:
                peak_times = np.array(time)[peaks]
                peak_values = np.array(processed_data)[peaks]
                
                # Interpolate between the peaks
                interp_time = np.linspace(min(time), max(time), 500)
                interp_values = np.interp(interp_time, peak_times, peak_values)
            else:
                print(f"No peaks found for {file_name} on {axis_label}")
                continue  # Skip to the next file if no peaks found
            
            # Plot the data
            color = next(chosen_colors)
            plt.plot(time, processed_data, label=f'{axis_label} - {file_name}', color=color, alpha=0.6)
            plt.scatter(peak_times, peak_values, color=color, marker='o', label=f'Peaks - {file_name}')
            plt.plot(interp_time, interp_values, color=color, linestyle='--', label=f'Interpolation - {file_name}')
        
        plt.title(f'{axis_label} Peaks and Interpolation')
        plt.xlabel('Time (s)')
        plt.ylabel(f'{axis_label} Amplitude')
        plt.legend()
    
    plt.tight_layout()
    plt.show()
