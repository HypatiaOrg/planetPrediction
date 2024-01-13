import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
from planetpred.table_read import ClassyReader
import sys
from datetime import datetime

set_name_one = 'setm12-drop'
set_name_two = 'setm16-drop'
experiment_name = 'Experiment 1'
ensemble_name_one = 'Ensemble 12'
ensemble_name_two = 'Ensemble 16'

# Define the Path Variables
path_one = os.path.dirname(os.path.realpath(__file__)) + '\\' + experiment_name + '\\' + set_name_one + '\\figures\\'
path_two = os.path.dirname(os.path.realpath(__file__)) + '\\' + experiment_name + '\\' + set_name_two + '\\figures\\'
output_dir = os.path.dirname(os.path.realpath(__file__)) + '\\Comparisons\\'

# Get the files to compare
file_one = path_one+'planet_probabilitiesFull-'+set_name_one+'.csv'
file_two = path_two+'planet_probabilitiesFull-'+set_name_two+'.csv'

elements_one = ['C', 'O', 'Na', 'Mg', 'Al', 'Si', 'Ca', 'Ti', 'V', 'Mn', 'Y', 'Cr', 'Ni']
elements_two = ['C', 'O', 'Na', 'Mg', 'Al', 'Si', 'Ca', 'Ti', 'V', 'Mn', 'Y', 'Cr', 'Ni', 'Fe']

plotXFe = False

hyp = ClassyReader("main.csv",delimiter=",")

predicted_one = ClassyReader(file_one,delimiter=",")
predicted_two = ClassyReader(file_two,delimiter=",")
element_dict_one = {}
element_dict_two = {}
element_dict_three = {}

# Open the two required files to see which stars have commonality
df_one = pd.read_csv(file_one)
df_two = pd.read_csv(file_two)

# Delete columns that aren't needed
del df_one['Sampled']
del df_one['Predicted']
del df_two['Sampled']
del df_two['Predicted']

# Rename the probability columns to coincide with each file
df_one = df_one.rename(columns={'Prob':'Prob 1'})
df_two = df_two.rename(columns={'Prob':'Prob 2'})

# Set the star_names as the index for each pandas array
df_one = df_one.set_index('star_name')
df_two = df_two.set_index('star_name')

# Concatenate both arrays
df = pd.concat([df_one, df_two],axis=1)

# Drop any rows with empty values
df = df.dropna()

# Make the star name column again and reset the indexes
df = df.rename_axis('star_name').reset_index()

for zz, n in enumerate(elements_one):
    element_dict_one[n] = {"pred":[]}
    element_dict_two[n] = {"pred":[]}
    element_dict_three[n] = {"pred":[]}
    predFe_one = []
    predFe_two = []
    predFe_three = []

    for zz, star in enumerate(hyp.star_name):
        if star in predicted_one.star_name:
            predFe_one.append(hyp.Fe[zz])
            if plotXFe:
                element_dict_one[n]["pred"].append(hyp.__getattribute__(n)[zz]-hyp.Fe[zz])
            else:
                element_dict_one[n]["pred"].append(hyp.__getattribute__(n)[zz])
        if star in predicted_two.star_name:
            predFe_two.append(hyp.Fe[zz])
            if plotXFe:
                element_dict_two[n]["pred"].append(hyp.__getattribute__(n)[zz]-hyp.Fe[zz])
            else:
                element_dict_two[n]["pred"].append(hyp.__getattribute__(n)[zz])
        #if star in (predicted_three.star_name):
        if star in list(df['star_name']):
            predFe_three.append(hyp.Fe[zz])
            if plotXFe:
                element_dict_three[n]["pred"].append(hyp.__getattribute__(n)[zz]-hyp.Fe[zz])
            else:
                element_dict_three[n]["pred"].append(hyp.__getattribute__(n)[zz])
    #Make the scatter plot.
    left, width = 0.13, 0.75
    bottom, height = 0.13, 0.75
    rect_scatter = [left, bottom, width, height]
    axScatter = plt.axes(rect_scatter)
    axScatter.scatter(predFe_one,element_dict_one[n]["pred"],s=30,marker="D",linewidths=0.5,facecolor="None",
                      edgecolor="red", label= ensemble_name_one + ' (≥90%)')
    axScatter.scatter(predFe_two,element_dict_two[n]["pred"],s=30,marker="D",linewidths=0.5,facecolor="None",
                      edgecolor="blue", label= ensemble_name_two + ' (≥90%)')
    axScatter.scatter(predFe_three,element_dict_three[n]["pred"],s=30,marker="D",linewidths=0.5,facecolor="None",
                      edgecolor="purple", label= ensemble_name_one + ' + ' + ensemble_name_two + ' (≥90%)')
    axScatter.set_facecolor('darkgrey')
    plt.title('Predicted Planet Hosts')
    
    # Adapt the labeling based on what's being plotted.
    axScatter.set_xlabel("[Fe/H]", fontsize=15)

    if plotXFe:
        if (n)=="Y":
            axScatter.set_ylabel("[Y/Fe]", fontsize=15)
        else:
            axScatter.set_ylabel("["+n+"/Fe]", fontsize=15)
    else:
        if (n) == "Y":
            axScatter.set_ylabel("[Y/H]", fontsize=15)
        else:
            axScatter.set_ylabel("["+n+"/H]", fontsize=15)

    if ((n) =="Mn" or not plotXFe):
        axScatter.legend(loc='upper left', scatterpoints=1,fontsize=8)
    else:
        axScatter.legend(loc='lower left', scatterpoints=1,fontsize=8)

    plt.show()
