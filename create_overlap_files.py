import numpy as np
import os
import pandas as pd
import matplotlib.pyplot as plt
import sys
from glob import glob
import venn
from planetpred.table_read import ClassyReader

#Define the path variable
path = os.path.dirname(os.path.realpath(__file__)) + '\\Current\\Validation Test\\'
### Open the main file
##df = pd.read_csv("main.csv",usecols=["star_name"])
##df = df.set_index('star_name')
##
### Iterate through every file in the ensemble
##count = 0
##for file in glob(path+"/planet_probabilitiesFull-*.csv"):
##    # Open the file
##    ensemble_run = pd.read_csv(file,usecols=['star_name', 'Sampled',
##                                             'Predicted', 'Prob'])
##    ensemble_run = ensemble_run.rename(columns={'Prob': 'Prob' + str(count)})
##    # Set the concat index to star names
##    ensemble_run = ensemble_run.set_index('star_name')
##    del ensemble_run['Sampled']
##    del ensemble_run['Predicted']
####    print(ensemble_run)
####    input()
##    # Concatenate the pandas series
##    df = pd.concat([df, ensemble_run], axis=1)
##    count+=1
##
##df = df.dropna()
### Check without Molar Ratio
##df = df[(df.Prob0 >= 0.9) & (df.Prob1 >= 0.9) & (df.Prob2 >= 0.9)
##        & (df.Prob3 >= 0.9) & (df.Prob4 >= 0.9) & (df.Prob5 >= 0.9)]
##### Check with Molar Ratio
####df = df[(df.Prob0 >= 0.9) & (df.Prob1 >= 0.9) & (df.Prob2 >= 0.9)
####        & (df.Prob3 >= 0.9) & (df.Prob4 >= 0.9) & (df.Prob5 >= 0.9)
####        & (df.Prob6 >= 0.9) & (df.Prob7 >= 0.9) & (df.Prob8 >= 0.9)
####        & (df.Prob9 >= 0.9) & (df.Prob10 >= 0.9)]
##
##
### Molar Ratio df
##df2 = pd.read_csv("main.csv",usecols=["star_name"])
##df2 = df2.set_index('star_name')
##
### Iterate through every file in the molar ratio ensemble
##count2 = 0
##for file in glob(path+"/planet_probabilitiesmr-*.csv"):
##    # Open the file
##    ensemble_run = pd.read_csv(file,usecols=['star_name', 'Sampled',
##                                             'Predicted', 'Prob'])
##    ensemble_run = ensemble_run.rename(columns={'Prob': 'Prob' + str(count2)})
##    # Set the concat index to star names
##    ensemble_run = ensemble_run.set_index('star_name')
##    del ensemble_run['Sampled']
##    del ensemble_run['Predicted']
####    print(ensemble_run)
####    input()
##    # Concatenate the pandas series
##    df2 = pd.concat([df2, ensemble_run], axis=1)
##    count2+=1
##
##df2 = df2.dropna()
### Check for Molar Ratio
##df2 = df2[(df2.Prob0 >= 0.9) & (df2.Prob1 >= 0.9) & (df2.Prob2 >= 0.9)
##        & (df2.Prob3 >= 0.9) & (df2.Prob4 >= 0.9)]
##
##### Check for Null sets
####df2 = df2[(df2.Prob0 >= 0.9) & (df2.Prob1 >= 0.9)]
##df = df.reset_index()
####df2 = df2.reset_index()
##
####labels = venn.get_labels([set(df['star_name'].unique()), set(df2['star_name'].unique())])
####fig,ax = venn.venn2(labels,names=['Ensembles 1-11', 'Ensembles 14-15'])
####plt.title('Null Test: Shared stars with Prob > 90%')
####plt.show()
####input()


# All df
df3 = pd.read_csv("main.csv",usecols=["star_name","Fe","C","O","Na",
                                      "Mg","Al","Si","Ca","Sc","Ti",
                                      "V","Cr","Mn","Co","Ni","Y",
                                      "C_Mg","O_Mg","Si_Mg","Ca_Mg","Ti_Mg","Fe_Mg",
                                      "C_Si","O_Si","Mg_Si","Ca_Si","Ti_Si","Fe_Si",
                                      "C_O","Si_O","Mg_O","Ca_O","Ti_O","Fe_O"])
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

### Check for null sets
##df3 = df3[(df3.Prob0 >= 0.9) & (df3.Prob1 >= 0.9) & (df3.Prob2 >= 0.9)
##          & (df3.Prob3 >= 0.9) & (df3.Prob4 >= 0.9) & (df3.Prob5 >= 0.9)
##          & (df3.Prob6 >= 0.9) & (df3.Prob7 >= 0.9) & (df3.Prob8 >= 0.9)
##          & (df3.Prob9 >= 0.9) & (df3.Prob10 >= 0.9) & (df3.Prob11 >= 0.9)
##          & (df3.Prob12 >= 0.9) & (df3.Prob13 >= 0.9) & (df3.Prob14 >= 0.9)]
##
##elements = ["Fe","C","O","Na","Mg","Al","Si","Ca","Sc",
##            "Ti","V","Cr","Mn","Co","Ni","Y"]
##plotXFe = False
##hyp = ClassyReader("main.csv",delimiter=",")
##element_dict = {}
##df3 = df3.rename_axis('star_name').reset_index()
##
###print(df3['star_name'])
##
##for zz, n in enumerate(elements):
##    element_dict[n] = {"pred":[]}
##    predFe=[]
##
##    for zz,star in enumerate(hyp.star_name):
##        if star in list(df['star_name']):
##            predFe.append(hyp.Fe[zz])
##            if plotXFe:
##                element_dict[n]["pred"].append(hyp.__getattribute__(n)[zz]-hyp.Fe[zz])
##            else:
##                element_dict[n]["pred"].append(hyp.__getattribute__(n)[zz])
##
##    left,width = 0.15, 0.75
##    bottom,height = 0.15, 0.75
##    rect_scatter = [left,bottom,width,height]
##    axScatter = plt.axes(rect_scatter)
##    axScatter.scatter(predFe,element_dict[n]["pred"],s=30,marker="o",linewidths=0.5,facecolor="red",
##                      edgecolor="red",label="Shared Stars (>90%)")
##    plt.title('Predicted Planet Hosts')
##    axScatter.set_xlabel("[Fe/H]",fontsize=15)
####    axScatter.set_facecolor('darkgrey')
##    if plotXFe:
##        if (n)=="Y":
##            axScatter.set_ylabel("[Y/Fe]",fontsize=15)
##        else:
##            axScatter.set_ylabel("["+n+"/Fe]",fontsize=15)
##    else:
##        if (n) == "Y":
##            axScatter.set_ylabel("[Y/H]",fontsize=15)
##        else:
##            axScatter.set_ylabel("["+n+"/H]",fontsize=15)
##    if ((n) == "Mn" or not plotXFe):
##        axScatter.legend(loc='upper left', scatterpoints=1,fontsize=8)
##    else:
##        axScatter.legend(loc='lower left',scatterpoints=1,fontsize=8)
##    plt.show()
##print(df3)
##input()
##df3 = df3.set_index('star_name')
df3.to_csv("big_overlap_experiment3.csv")
