import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from planetpred.table_read import ClassyReader
from matplotlib_venn import venn2,venn2_circles

import venn

set_name_one = 'set1-null'
set_name_two = 'set2-null'
set_name_three = 'set3-null'
set_name_four = 'set4-null'
experiment_name = 'Experiment 3'
ensemble_name_one = 'Ensemble 1'
ensemble_name_two = 'Ensemble 2'
ensemble_name_three = 'Ensemble 3'
ensemble_name_four = 'Ensemble 4'

# Define the Path Variables
path_one = os.path.dirname(os.path.realpath(__file__)) + '\\' + experiment_name + '\\' + set_name_one + '\\figures\\'
path_two = os.path.dirname(os.path.realpath(__file__)) + '\\' + experiment_name + '\\' + set_name_two + '\\figures\\'
path_three = os.path.dirname(os.path.realpath(__file__)) + '\\' + experiment_name + '\\' + set_name_three + '\\figures\\'
path_four = os.path.dirname(os.path.realpath(__file__)) + '\\' + experiment_name + '\\' + set_name_four + '\\figures\\'

# Get the files to compare
file_one = path_one+'planet_probabilitiesFull-'+set_name_one+'.csv'
file_two = path_two+'planet_probabilitiesFull-'+set_name_two+'.csv'
file_three = path_three+'planet_probabilitiesFull-'+set_name_three+'.csv'
file_four = path_four+'planet_probabilitiesFull-'+set_name_four+'.csv'

df_one = pd.read_csv(file_one)
df_two = pd.read_csv(file_two)
df_three = pd.read_csv(file_three)
df_four = pd.read_csv(file_four)

del df_one['Sampled']
del df_one['Predicted']
del df_one['Prob']
del df_two['Sampled']
del df_two['Predicted']
del df_two['Prob']
del df_three['Sampled']
del df_three['Predicted']
del df_three['Prob']
del df_four['Sampled']
del df_four['Predicted']
del df_four['Prob']

labels = venn.get_labels([set(df_one['star_name'].unique()),
                          set(df_two['star_name'].unique()),
                          set(df_three['star_name'].unique()),
                          set(df_four['star_name'].unique())])
fig, ax = venn.venn4(labels, names=['Ensemble 1', 'Ensemble 2', 'Ensemble 3', 'Ensemble 4'])
plt.title('Experiment 1: Shared stars with Prob > 90%')
fig.show()
