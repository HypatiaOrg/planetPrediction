import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import sys
from glob import glob
from planetpred.table_read import ClassyReader

#Define the path variable
path = os.path.dirname(os.path.realpath(__file__)) + '\\Current\\Experiment 3\\'
# All df
df3 = pd.read_csv("main - Copy.csv",usecols=["star_name","Fe","C","O","Na",
                                      "Mg","Al","Si","Ca","Sc","Ti",
                                      "V","Cr","Mn","Co","Ni","Y",
                                      "C_Mg","O_Mg","Si_Mg","Ca_Mg","Ti_Mg","Fe_Mg",
                                      "C_Si","O_Si","Mg_Si","Ca_Si","Ti_Si","Fe_Si",
                                      "C_O","Si_O","Mg_O","Ca_O","Ti_O","Fe_O","f_disk","f_disk_2"],
                  na_filter = False)
df3 = df3.set_index('star_name')

# Iterate through every file in the ensemble
count3 = 0
for file in glob(path+"/planet_probabilitiese3*.csv"):
    # Open the file
    ensemble_run = pd.read_csv(file,usecols=['star_name', 'Sampled',
                                             'Predicted', 'Prob'])
    ensemble_run = ensemble_run.rename(columns={'Prob': 'Prob' + str(count3)})
    # Set the concat index to star names
    ensemble_run = ensemble_run.set_index('star_name')
    del ensemble_run['Sampled']
    del ensemble_run['Predicted']
    
    # Concatenate the pandas series
    df3 = pd.concat([df3, ensemble_run], axis=1)
    count3+=1
# Check for non-null sets
df3 = df3[(df3.Prob0 >= 0.9) & (df3.Prob1 >= 0.9) & (df3.Prob2 >= 0.9)
          & (df3.Prob3 >= 0.9) & (df3.Prob4 >= 0.9) & (df3.Prob5 >= 0.9)
          & (df3.Prob6 >= 0.9)]
df3.to_csv("big_overlap_experiment3.csv")
