import ndtest
import numpy as np
import pandas as pd


overlap_filename = "big_overlap_experiment2.csv"
output_filename = "ks_test_e2.csv"

# Open the files
df_main = pd.read_csv("main - Copy.csv",usecols=["Fe","C","O","Na","Mg","Al","Si",
                                          "Ca","Sc","Ti","V","Cr","Mn","Co",
                                          "Ni","Y","f_disk_2"])

df_over = pd.read_csv(overlap_filename)

# Define empty lists to store values later on...
p_values = []
features = []

def ks_elements(features, p_values):

    for column in df_main.columns:
        if (column == "Sc" or column == "Co" or column == "f_disk_2"):
            continue
        else:
            # Create a temp series that drops nulls in the relevant column
            temp_main = df_main.dropna(subset=[column])

            if overlap_filename == "big_overlap_experiment3.csv":
                temp_over = df_over.dropna(subset=[column])
                ndarray_over_fe = temp_over["Fe"].to_numpy()
                ndarray_over_column = temp_over[column].to_numpy()
            else:
                ndarray_over_fe = df_over["Fe"].to_numpy()
                ndarray_over_column = df_over[column].to_numpy()

            # Change datatype to ndarray so it works with ks2d2s...
            ndarray_main_fe = temp_main["Fe"].to_numpy()
##            ndarray_over_fe = df_over["Fe"].to_numpy()
            ndarray_main_column = temp_main[column].to_numpy()
##            ndarray_over_column = df_over[column].to_numpy()
        # Perform the KS Test
        P, D = ndtest.ks2d2s(ndarray_main_fe, ndarray_main_column, ndarray_over_fe,
                             ndarray_over_column,extra=True)
        # Append to relevant columns
        features.append(column)
        p_values.append(P)

##    # Create series for output:
##    df = pd.DataFrame({'Feature': features,
##                       'p-value': p_values})
##
##    # Output
##    df = df.set_index('Feature')
##    df.to_csv(output_filename)
    return

def ks_disk():
    ndarray_main_fe = df_main["Fe"].to_numpy()
    ndarray_main_disk = df_main["f_disk_2"].to_numpy()
    ndarray_over_fe = df_over["Fe"].to_numpy()
    ndarray_over_disk = df_over["f_disk_2"].to_numpy()
    P,D = ndtest.ks2d2s(ndarray_main_fe, ndarray_main_disk, ndarray_over_fe,
                        ndarray_over_disk,extra=True)
    print(f"{P=:.3g}, {D=:.3g}")
    features.append("disk")
    p_values.append(P)
    return

def check_for_na():
    for column in df_main.columns:
        if df_over[column].isnull().values.any():
            print(column)
    return

def output_file(features,p_values):
    # Create series for output:
    df = pd.DataFrame({'Feature': features,
                       'p-value': p_values})

    # Output
    df = df.set_index('Feature')
    df.to_csv(output_filename)
    return

ks_elements(features,p_values)
ks_disk()
output_file(features,p_values)
