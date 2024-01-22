import numpy as np
import os
import pandas as pd
import sys
from scipy.stats import anderson_ksamp
from planetpred.table_read import ClassyReader

# Read the input data sets
df_main = pd.read_csv("main.csv",usecols=["Fe","C","O","Na","Mg","Al","Si",
                                          "Ca","Sc","Ti","V","Cr","Mn","Co",
                                          "Ni","Y"])
df_over = pd.read_csv("big_overlap_experiment1.csv")

# Define the values to output
features = np.array(df_main.columns)
statistics = []
p_values = []

# AD Test between the overlap [Fe/H] and main [Fe/H]
res = anderson_ksamp([df_main["Fe"],df_over["Fe"]])
##print(res.statistic, res.pvalue)
##print(res.critical_values)

features = np.append("Fe", features)
statistics.append(res.statistic)
p_values.append(res.pvalue)

# AD Test between the [Fe/H] after nulls removed for [X/H] elements in main dataset and main [Fe/H]
for column in df_main.columns:
    # Create a temporary series that drops nulls in the relevant column
    temp = df_main.dropna(subset=[column])
    # AD Test using the [Fe/H] values remaining in temp after [X/H] null removal
    temp_res = anderson_ksamp([df_main["Fe"],temp["Fe"]])
    statistics.append(temp_res.statistic)
    p_values.append(temp_res.pvalue)

# Create a series for output
df = pd.DataFrame({'Feature': features,
                   'Statistics': statistics,
                   'p-value': p_values})

# Output the file
df = df.set_index('Feature')
df.to_csv('ad_test.csv')
