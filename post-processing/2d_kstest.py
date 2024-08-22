import ndtest
import numpy as np
import pandas as pd


output_filename = "ks_sample_ex3.csv"

# Open the files
df_main = pd.read_csv("combined_data-20240814.csv",usecols=["Experiment","Overlap Star",
                                                            "[Fe/H]","[C/H]","[O/H]",
                                                            "[Na/H]","[Mg/H]","[Al/H]",
                                                            "[Si/H]","[Ca/H]","[Sc/H]",
                                                            "[Ti/H]","[V/H]","[Cr/H]",
                                                            "[Mn/H]","[Co/H]","[Ni/H]",
                                                            "[Y/H]","Disk Location"])
df_main["Disk Location"] = df_main["Disk Location"].fillna(0)

# Define empty lists to store values later on...
p_values = []
features = []
length_main = []
length_over = []

def ks_elements(features, p_values, experiment):

    for column in df_main.columns:
        if (column == "Experiment" or column == "Overlap Star" or
            column == "[Sc/H]" or column == "[Co/H]"):
            continue
        else:
            # Create a temp series that drops nulls in the relevant column
            temp_main = df_main[(df_main['Experiment'] == experiment)].dropna(subset=[column])

            if experiment == 3:
                temp_over = df_main[(df_main['Overlap Star'] == 'Yes') &
                                    (df_main['Experiment'] == 3)].dropna(subset=[column])
                ndarray_over_fe = temp_over["[Fe/H]"].to_numpy()
                ndarray_over_column = temp_over[column].to_numpy()
            else:
                ndarray_over_fe = df_main[(df_main['Overlap Star'] == 'Yes') &
                                          (df_main['Experiment'] == experiment)]["[Fe/H]"].to_numpy()
                ndarray_over_column = df_main[(df_main['Overlap Star'] == 'Yes') &
                                              (df_main['Experiment'] == experiment)][column].to_numpy()

            # Change datatype to ndarray so it works with ks2d2s...
            ndarray_main_fe = temp_main["[Fe/H]"].to_numpy()
            ndarray_main_column = temp_main[column].to_numpy()
            
        # Perform the KS Test
        P, D = ndtest.ks2d2s(ndarray_main_fe, ndarray_main_column, ndarray_over_fe,
                             ndarray_over_column,extra=True)
        # Append to relevant columns
        features.append(column)
        p_values.append(P)
        length_main.append(len(ndarray_main_fe))
        length_over.append(len(ndarray_over_fe))
    return

def output_file(features,p_values):
    # Create series for output:
    df = pd.DataFrame({'Feature': features,
                       'p-value': p_values,
                       'Sample Main': length_main,
                       'Sample Over': length_over})

    # Output
    df = df.set_index('Feature')
    df.to_csv(output_filename)
    return

ks_elements(features,p_values,3)
output_file(features,p_values)
