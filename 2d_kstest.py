import ndtest
import numpy as np
import pandas as pd

# Open the files
df_main = pd.read_csv("main.csv",usecols=["Fe","C","O","Na","Mg","Al","Si",
                                          "Ca","Sc","Ti","V","Cr","Mn","Co",
                                          "Ni","Y"])

df_over = pd.read_csv("big_overlap_experiment1.csv")

# Define empty lists to store values later on...
p_values = []
features = []

for column in df_main.columns:
    if (column == "Sc" or column == "Co"):
        continue
    else:
        # Create a temp series that drops nulls in the relevant column
        temp_main = df_main.dropna(subset=[column])

        # Change datatype to ndarray so it works with ks2d2s...
        ndarray_main_fe = temp_main["Fe"].to_numpy()
        ndarray_over_fe = df_over["Fe"].to_numpy()
        ndarray_main_column = temp_main[column].to_numpy()
        ndarray_over_column = df_over[column].to_numpy()
    # Perform the KS Test
    P, D = ndtest.ks2d2s(ndarray_main_fe, ndarray_main_column, ndarray_over_fe,
                         ndarray_over_column,extra=True)
    # Append to relevant columns
    features.append(column)
    p_values.append(P)

# Create series for output:
df = pd.DataFrame({'Feature': features,
                   'p-value': p_values})

# Output
df = df.set_index('Feature')
df.to_csv('ks_test.csv')
