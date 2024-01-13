import numpy as np
import os
import pandas as pd
import matplotlib as plt
import sys
from glob import glob

path = os.path.dirname(os.path.realpath(__file__)) + '\\Total Probabilities\\'
path2 = os.path.dirname(os.path.realpath(__file__)) + '\\Supplemental Material\\'

# Define the main dataframe
df = pd.read_csv("main.csv", usecols=["star_name"])
# Iterate through every iteration of the ensemble
for file in glob(path+"/planet_probabilitiesTotal-*.csv"):
    # Open the file
    ensemble_run = pd.read_csv(file)
    # Add the values for Sampled together and Predicted together based on the Star Names
    df = df.set_index('star_name').add(ensemble_run.set_index('star_name'), fill_value=0).reset_index()
    del df['Predicted']
    del df['Sampled']

df = df.set_index('star_name')
df.to_csv(path2+'Probabilities_Experiment3.csv')
