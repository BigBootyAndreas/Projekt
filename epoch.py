import csv
import time
path 
# Function to convert epoch to milliseconds
def convert_to_milliseconds(epoch):
    try:
        return int(epoch) * 1000
    except ValueError:
        print(f"Invalid epoch value: {epoch}")
        return None

# Path to the CSV file
file_path = 'input.csv'  # Change this to your actual file path

# Reading the CSV file
with open(file_path, 'r') as csv_file:
    reader = csv.reader(csv_file)
    header = next(reader)  # Reading the header if present
    
    print("Converting epoch values from the 4th column to milliseconds...")
    
    for row in reader:
        if len(row) >= 4:  # Ensure the row has at least 4 columns
            epoch_value = row[3]
            epoch_in_ms = convert_to_milliseconds(epoch_value)
            
            if epoch_in_ms is not None:
                print(f"Original: {epoch_value}, Converted: {epoch_in_ms}")

# Note: To save the output to a new CSV file, you can modify this script accordingly.
