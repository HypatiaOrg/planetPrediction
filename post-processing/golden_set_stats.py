import os
import pandas as pd
from glob import glob

# Define base path and experiment identifier
base_path = r'C:\Users\Locuan\Documents\GitHub\planetPrediction-New\experiment-3'

# Initialize an empty list to hold DataFrames
data_frames = []

# Iterate through all set folders (set1, set2, set3, ...)
for set_number in range(1, 7):  # Assuming there could be up to 99 sets
    set_path = os.path.join(base_path, f'set{set_number}\\figures')
    if not os.path.exists(set_path):
        break  # Stop if the folder doesn't exist

    # Find all CSV files with the desired pattern in the current set folder
    for file in glob(os.path.join(set_path, "goldenSetProbabilities*.csv")):
        golden_file = pd.read_csv(file, usecols=["star_name", "Sampled", "Predicted", "Prob"])
        data_frames.append(golden_file)

# Concatenate all DataFrames in one go
df = pd.concat(data_frames, ignore_index=True)

# Save the concatenated DataFrame to the experiment-1 folder
output_file_path = os.path.join(base_path, "golden_set_all.csv")
df.to_csv(output_file_path, index=False)
