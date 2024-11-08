import numpy as np
import sounddevice as sd
import datetime
import threading
import queue as QueueModule # Rename the queue module to avoid conflict
import os
import time
from google.cloud import storage

#Text colors
CYELLOW = '\033[93m'
CGREEN = '\033[92m'
CBLUE = '\033[94m'
CRED = '\033[91m'
CBLINK = '\033[5m'
CEND = '\033[0m'


def record_audio(duration, samplerate, channels, data_queue):
    
    # Record audio
    
    print("Recording started")

    recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype="float32")

    sd.wait() # Wait until recording is finished

    print(f"Recording finished. Size of recording: {recording.shape}")
    data_queue.put(recording)

    print("\nempty: ", data_queue.qsize())

def save_segment(filename, recording, time_values, segment_start_time):

    # Save segment data to file or any other storage method
    print(f"Saving segment: {filename}")

    # Add time values to array
    data = np.column_stack((time_values, recording))

    # Create timestamps
    timestamps = [(segment_start_time +
    datetime.timedelta(seconds=time_values[i])).strftime("%Y-%m-%d %H:%M:%S") for
    i in range(len(recording))]
    path = "C:\\Users\\Ali\\OneDrive - Aalborg Universitet\\Desktop\\P7\\Projekt\\recorder\\segments\\"

    # Add timestamp column to the data
    data_with_timestamp = np.column_stack((timestamps, data))
    np.savez_compressed(path+filename, a=data_with_timestamp)
    print(CGREEN + f"Segment {filename} saved" + CEND)

    BUCKET_NAME = "aau_vt1"
    CREDENTIALS_FILE = "C:\\Users\\Ali\\OneDrive - Aalborg Universitet\\Desktop\\P7\\Projekt\\recorder\\euphoric-anchor-439706-k3-d5147822d8ac.json"
    upload_thread = threading.Thread(target=upload_to_gcs, args=(BUCKET_NAME, path + filename + r".npz",
        filename + r".npz", CREDENTIALS_FILE, filename))
    upload_thread.start()


def upload_to_gcs(bucket_name, source_file_path, destination_blob_name, credentials_file, filename):

    print("Uploading file " + filename)

    COUNTER_FILE = "C:\\Users\\Ali\\OneDrive - Aalborg Universitet\\Desktop\\P7\\Projekt\\recorder\\counter.txt"

    # Initialize the Google Cloud Storage client with the credentials
    storage_client = storage.Client.from_service_account_json(credentials_file)

    # Locate txt file and read current data set and run numbers
    with open(COUNTER_FILE, "r") as f:
        counter, data_set = map(int, f.read().split())

    # Check if 12 runs is reached and make update the data set if true
    if counter % 12 == 0:
        print(f"Run {counter}: Data{data_set}")
        data_set += 1
    else:
        print(f"Run {counter}: Data{data_set}")

    # Get the target bucket
    bucket = storage_client.bucket(bucket_name)

    # Upload the file to the bucket
    blob = bucket.blob(f"audio/data{data_set}/run{counter}_{destination_blob_name}")
    blob.upload_from_filename(source_file_path)

    print(CBLUE + f"File {source_file_path} uploaded to gs://{bucket_name}/audio/data{data_set}/run{counter}_{destination_blob_name}" + CEND)

    if os.path.exists(source_file_path):
        os.remove(source_file_path)
        print(CRED + filename + " removed" + CEND)
    else:
        print("File doesn't exist")

    # Increment counter and update the txt file
    counter += 1
    with open(COUNTER_FILE, "w") as f:
        f.write(f"{counter} {data_set}")

def main():
    segment_duration_seconds = 60
    samplerate = 16000
    channels = 1
    #segments = 3

# Create a queue for communication between threads
    data_queue = QueueModule.Queue(maxsize=0)

    while True:

        segment_start_time = datetime.datetime.now()
        segment_filename = f"segment_{segment_start_time.strftime("%Y%m%d_%H%M%S")}"

        # Start the recording thread
        recording_thread = threading.Thread(target=record_audio,
        args=(segment_duration_seconds, samplerate, channels, data_queue))
        recording_thread.start()

        # Retrieve the recorded data from the queue and start the saving thread
        recording_thread.join()
        recording = data_queue.get() 

        # Retrieve the data from the queue
        time_values = np.linspace(0, segment_duration_seconds, len(recording))
        saving_thread = threading.Thread(target=save_segment, args=(segment_filename,
        recording, time_values, segment_start_time))
        print(len(recording))
        saving_thread.start()

if __name__ == "__main__":
    main()