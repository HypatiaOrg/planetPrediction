import numpy as np
import sys
import os
import pandas as pd
from glob import glob

def process_probabilities(experiment, set_name):
    # Define file locations
    work_dir = os.path.dirname(os.path.realpath(__file__))
    path = os.path.join(work_dir, experiment, set_name, 'figures')
    output_dir = os.path.join(work_dir, 'Total Probabilities')

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Define the main dataframe
    df = pd.read_csv("main.csv", usecols=["star_name"])
    df['Sampled'] = 0
    df['Predicted'] = 0

    # Iterate through every iteration of the ensemble
    for file in glob(os.path.join(path, "planet_probabilitiesAll-*.csv")):
        # Open the file
        ensemble_run = pd.read_csv(file, usecols=["star_name", 'Sampled', 'Predicted'])
        # Add the values for Sampled and Predicted together based on the Star Names
        df = df.set_index('star_name').add(ensemble_run.set_index('star_name'), fill_value=0).reset_index()

    # Determine the total probability for each star
    df['Probability'] = df.apply(lambda row: row['Predicted'] / row['Sampled'] if row['Sampled'] > 0 else 'nan', axis=1)

    # Set the index for the dataframe
    df = df.set_index('star_name')

    # Output the file
    output_file = os.path.join(output_dir, f'p-total-{experiment}-{set_name}.csv')

    df.to_csv(output_file)
    print("File saved:", output_file)

process_probabilities("experiment-3", "set7")
