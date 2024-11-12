import os
import pandas as pd

def segmentation_analysis(input_dir, window, step_size, rate_hz, sample_dir, output_dir, amp_tol, amp_var_tol):

    def calculate_reference_features(sample):
        amplitude_data = sample.iloc[:, 2]
        return {
            "mean_amplitude": amplitude_data.mean(),
            "amplitude_variance": amplitude_data.var(),
        }

    # Reference sample files
    reference_sample_files = [f for f in os.listdir(sample_dir) if "sample" in f and f.endswith(".csv")]

    # Load each reference sample as a DataFrame and compute its mean and variance
    reference_samples = [pd.read_csv(os.path.join(sample_dir, sample)) for sample in reference_sample_files]

    # Create list of reference features for each sample
    reference_features = [calculate_reference_features(sample) for sample in reference_samples]

    # Define matching tolerances for amplitude
    amplitude_tolerance = amp_tol
    amplitude_variance_tolerance = amp_var_tol

    # Sampling parameters
    sample_rate = rate_hz  # in Hz
    window_samples = window * sample_rate  # 30 seconds of samples (480,000 samples at 16kHz)
    step_samples = step_size * sample_rate  # step by 5 seconds (80,000 samples at 16kHz)

    # Process each 5-minute data file
    files = sorted([f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f)) and f.endswith(".csv")])

    for file_name in files:
        print(f"Processing file: {file_name}")
        file_path = os.path.join(input_dir, file_name)
        data = pd.read_csv(file_path)

        # Sliding window over the data in sample counts
        start_index = 0
        matching_segments = []

        while start_index + window_samples <= len(data):
            # Extract the window segment of 30 seconds (480,000 samples)
            window_data = data.iloc[start_index : start_index + window_samples]
            
            # Extract amplitude data from the third column
            amplitude_data = window_data.iloc[:, 2]

            # Calculate features for the current window
            window_features = {
                "mean_amplitude": amplitude_data.mean(),
                "amplitude_variance": amplitude_data.var(),
            }

            # Compare window features with each reference sample
            for ref_idx, ref_features in enumerate(reference_features):
                amplitude_diff = abs(window_features["mean_amplitude"] - ref_features["mean_amplitude"])
                amplitude_variance_diff = abs(window_features["amplitude_variance"] - ref_features["amplitude_variance"])

                if amplitude_diff <= amplitude_tolerance and amplitude_variance_diff <= amplitude_variance_tolerance:
                    print(f"Match found for reference {ref_idx+1} in file {file_name} at sample index {start_index}")

                    # Save matching segment details
                    matching_segments.append({
                        "start_sample": start_index,
                        "end_sample": start_index + window_samples,
                        "reference_id": ref_idx + 1,
                        "file_name": file_name
                    })

            # Move the sliding window
            start_index += step_samples

        # Save results to a file
        if matching_segments:
            result_filename = os.path.join(output_dir, f"matches_{file_name}")
            results_df = pd.DataFrame(matching_segments)
            results_df.to_csv(result_filename, index=False)
            print(f"Matching segments saved to {result_filename}")
        else:
            print("No matches found in this file.")
