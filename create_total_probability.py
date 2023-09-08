import numpy as np
import os
import pandas as pd
import matplotlib as plt
import sys
from glob import glob

## Useful links
## https://www.geeksforgeeks.org/reading-specific-columns-of-a-csv-file-using-pandas/
## https://www.geeksforgeeks.org/how-to-add-empty-column-to-dataframe-in-pandas/
## https://stackoverflow.com/questions/49111859/how-to-merge-two-dataframes-and-sum-the-values-of-columns
## https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.to_csv.html

# Define file locations
experiment = 'Experiment 1'
set_name = 'setm13-drop'
work_dir = os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(os.path.realpath(__file__)) + '\\' + experiment + '\\' + set_name + '\\figures\\'

# Define the main dataframe
df = pd.read_csv("main.csv", usecols=["star_name"])
df['Sampled'] = np.nan
df['Predicted'] = np.nan

# Iterate through every iteration of the ensemble
for file in glob(path+"/planet_probabilitiesAll-*.csv"):
    # Open the file
    ensemble_run = pd.read_csv(file,usecols=["star_name", 'Sampled', 'Predicted'])
    # Add the values for Sampled together and Predicted together based on the Star Names
    df = df.set_index('star_name').add(ensemble_run.set_index('star_name'), fill_value=0).reset_index()

# Determine the total probability for each star
df['Prob'] = df['Predicted']/df['Sampled']

# Define the Star Names as the indexes of the Data Frame
df = df.set_index('star_name')

# Drop null value rows
df = df.dropna()
df = df[df.Prob >= 0.9]

# Output the file
df.to_csv(path+'planet_probabilitiesFull'+'-'+set_name+'.csv')
