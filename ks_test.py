import numpy as np
import os
import pandas as pd
import sys
from scipy.stats import kstest, ks_2samp
from planetpred.table_read import ClassyReader

# Read the input data sets
df_main = pd.read_csv("main.csv",usecols=["Fe","C","O","Na","Mg","Al","Si",
                                          "Ca","Sc","Ti","V","Cr","Mn","Co",
                                          "Ni","Y"])
df_over = pd.read_csv("big_overlap_experiment1.csv")

# Define the values to output
features = np.array(df_main.columns)
p_values = []

# KS Test between the overlap [Fe/H] and main [Fe/H]
p_values.append(ks_2samp(df_main["Fe"],df_over["Fe"])[1])
features = np.append("Fe", features)

# KS Test between the [Fe/H] after nulls removed for [X/H] elements in main dataset and main [Fe/H]
for column in df_main.columns:
    # Create a temporary series that drops nulls in the relevant column
    temp = df_main.dropna(subset=[column])
    # KS Test using the [Fe/H] values remaining in temp after [X/H] null removal
    p_values.append(ks_2samp(df_main["Fe"], temp["Fe"])[1])

# Create a series for output
df = pd.DataFrame({'Feature': features,
                   'p-value': p_values})

# Output the file
df = df.set_index('Feature')
df.to_csv('ks_test.csv')
