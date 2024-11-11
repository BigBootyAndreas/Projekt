import csv
import matplotlib.pyplot as plt
from datetime import datetime

# Path to the CSV file
#file_path = r"C:\\Users\\Ali\\OneDrive - Aalborg Universitet\\Desktop\\P7\\Data\\IMU\\IMU.csv"

#test

# Initialize lists to store data for plotting
x_values = []
y_values = []
z_values = []
time_values = []

# Reading the CSV file
def IMU_analysis(subdirs,directory):
    with open(directory, 'r') as csv_file:
     reader = csv.reader(csv_file)
    header = next(reader)  # Skip header if present
    
    for row in reader:
        if len(row) >= 4:  # Ensure the row has at least 5 columns
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

    # Plotting the graphs
    plt.figure(figsize=(14, 8))

    # Plot for x vs. time
    plt.subplot(3, 1, 1)
    plt.plot(time_values, x_values, label='X Values', color='r')
    plt.title('X vs. Time')
    plt.xlabel('Time (s)')
    plt.ylabel('X')

    # Plot for y vs. time
    plt.subplot(3, 1, 2)
    plt.plot(time_values, y_values, label='Y Values', color='g')
    plt.title('Y vs. Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Y')

    # Plot for z vs. time
    plt.subplot(3, 1, 3)
    plt.plot(time_values, z_values, label='Z Values', color='b')
    plt.title('Z vs. Time')
    plt.xlabel('Time (s)')
    plt.ylabel('Z')

    plt.tight_layout()  # Adjusts spacing to prevent overlap
    plt.show()
