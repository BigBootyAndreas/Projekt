import pandas as pd
import matplotlib.pyplot as plt


csv_path = 'C:\\Users\\Ali\\OneDrive - Aalborg Universitet\\Desktop\\P7\\Data\\data4\\run0_segment_20241108_102620.csv'  # Replace this with the actual file path
def plot_time_frequency(csv_path):
    # Read the CSV file
    data = pd.read_csv(csv_path)

    # Extract time and frequency columns
    time_data = data.iloc[:, 1]  # Column 2 for time
    frequency_data = data.iloc[:, 2]  # Column 3 for frequency

    # Plot time vs. frequency
    plt.figure(figsize=(10, 6))
    plt.plot(time_data, frequency_data, color='b', label='Frequency Data')
    plt.title('Time vs. Frequency Data')
    plt.xlabel('Time')
    plt.ylabel('Frequency')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

# Define the path to your CSV file


# Call the function to plot the data
plot_time_frequency(csv_path)
