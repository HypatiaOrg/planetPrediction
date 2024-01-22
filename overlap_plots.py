import numpy as np
import os
import pandas as pd
import sys
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from glob import glob
from planetpred.table_read import ClassyReader
from datetime import datetime

#Define the path variable
path = os.path.dirname(os.path.realpath(__file__)) + '\\Current\\Experiment 1\\'
# Open the main file
df = pd.read_csv("main.csv",usecols=["star_name","Fe","C","O","Na",
                                      "Mg","Al","Si","Ca","Sc","Ti",
                                      "V","Cr","Mn","Co","Ni","Y"])
df = df.set_index('star_name')

def create_series(df, partial_filename, isMolar):
    count = 0
    for file in glob(path+"/"+partial_filename+"*.csv"):
        ensemble_run = pd.read_csv(file,usecols=['star_name', 'Sampled',
                                                 'Predicted', 'Prob'])
        ensemble_run = ensemble_run.rename(columns={'Prob': 'Prob' + str(count)})
        ensemble_run = ensemble_run.set_index('star_name')
        del ensemble_run['Sampled']
        del ensemble_run['Predicted']
        df = pd.concat([df,ensemble_run],axis=1)
        count+=1
    #df = df.rename_axis('star_name').reset_index()
    # Is there a way to not hardcode this?
    if 'molar':
        df = df[(df.Prob0 >= 0.9) & (df.Prob1 >= 0.9) & (df.Prob2 >= 0.9)
              & (df.Prob3 >= 0.9) & (df.Prob4 >= 0.9)]
    elif 'non-molar':
        df = df[(df.Prob0 >= 0.9) & (df.Prob1 >= 0.9) & (df.Prob2 >= 0.9)
              & (df.Prob3 >= 0.9) & (df.Prob4 >= 0.9) & (df.Prob5 >= 0.9)]
    elif 'all':
        df = df[(df.Prob0 >= 0.9) & (df.Prob1 >= 0.9) & (df.Prob2 >= 0.9)
              & (df.Prob3 >= 0.9) & (df.Prob4 >= 0.9) & (df.Prob5 >= 0.9)
              & (df.Prob6 >= 0.9) & (df.Prob7 >= 0.9) & (df.Prob8 >= 0.9)
              & (df.Prob9 >= 0.9) & (df.Prob10 >= 0.9)]
    return df

def plot_abundance(df, plotXFe):
    elements = ["Fe","C","O","Na","Mg","Al","Si","Ca","Sc",
                "Ti","V","Cr","Mn","Co","Ni","Y"]
    hyp = ClassyReader("main.csv",delimiter=",")
    element_dict = {}
    df = df.rename_axis('star_name').reset_index()

    for zz, n in enumerate(elements):
        element_dict[n] = {"pred":[]}
        predFe=[]

        for zz, star in enumerate(hyp.star_name):
            if star in list(df['star_name']):
                predFe.append(hyp.Fe[zz])
                if plotXFe:
                    element_dict[n]["pred"].append(hyp.__getattribute__(n)[zz]-hyp.Fe[zz])
                else:
                    element_dict[n]["pred"].append(hyp.__getattribute__(n)[zz])
        left,width = 0.15, 0.75
        bottom,height = 0.15, 0.75
        rect_scatter = [left,bottom,width,height]
        axScatter = plt.axes(rect_scatter)
        axScatter.scatter(predFe,element_dict[n]["pred"],s=30,marker="o",linewidths=0.5,facecolor="None",
                      edgecolor="#1E88E5",label="Shared Stars (≥90%)")
        plt.title('Predicted Planet Hosts')
        axScatter.set_xlabel("[Fe/H]",fontsize=15)

        if plotXFe:
            if (n)=="Y":
                axScatter.set_ylabel("[Y/Fe]",fontsize=15)
            else:
                axScatter.set_ylabel("["+n+"/Fe]",fontsize=15)
        else:
            if (n) == "Y":
                axScatter.set_ylabel("[Y/H]",fontsize=15)
            else:
                axScatter.set_ylabel("["+n+"/H]",fontsize=15)
        if ((n) == "Mn" or not plotXFe):
            axScatter.legend(loc='upper left',scatterpoints=1,fontsize=8)
        else:
            axScatter.legend(loc='lower left',scatterpoints=1,fontsize=8)
        plt.savefig(os.path.join('C:\\Users\\Locuan\\Documents\\GitHub\\planetPrediction\\Abundance Shared\\',
                                 "predicted"+n+"H"+str(datetime.today().strftime('-%h%d-%H%M%S'))+".pdf"))
        plt.close()
##        plt.show()
    return

def plot_molar(df):
    molar_ratios = ["C_Mg","O_Mg","Si_Mg","Ca_Mg","Ti_Mg","Fe_Mg","C_Si","O_Si",
                    "Mg_Si","Ca_Si","Ti_Si","Fe_Si","C_O","Si_O","Mg_O","Ca_O",
                    "Ti_O","Fe_O"]
    hyp = ClassyReader("main.csv",delimiter=",")
    plotAgainst = hyp.Fe
    molar_dict = {}
    df = df.rename_axis('star_name').reset_index()

    for zz, n in enumerate(molar_ratios):
        molar_dict[n] = {"pred": []}
        predFe = []

        for zz, star in enumerate(hyp.star_name):
            if star in list(df['star_name']):
                predFe.append(plotAgainst[zz])
                molar_dict[n]["pred"].append(hyp.__getattribute__(n)[zz])
        left,width = 0.15, 0.75
        bottom,height = 0.15, 0.75
        rect_scatter = [left,bottom,width,height]
        axScatter = plt.axes(rect_scatter)
        axScatter.scatter(predFe,molar_dict[n]["pred"],s=30,marker="o",linewidths=0.5,facecolor="None",
                      edgecolor="#1E88E5",label="Shared Stars (≥90%)")
        plt.title('Predicted Planet Hosts')
        axScatter.set_ylabel(n.replace("_","/"),fontsize=15)
        # If not [Fe/H] replace bottom line.
        axScatter.set_xlabel("[Fe/H]",fontsize=15)
        axScatter.legend(loc='upper left',scatterpoints=1,fontsize=8)
        plt.savefig(os.path.join('C:\\Users\\Locuan\\Documents\\GitHub\\planetPrediction\\Abundance Molar\\',
                                 "predicted"+n+str(datetime.today().strftime('-%h%d-%H%M%S'))+".pdf"))
        plt.close()
##        plt.show()
    return

def ensemble_comp(df1,df2,check):
    if check == True:
        plot_var = ["C_Mg","O_Mg","Si_Mg","Ca_Mg","Ti_Mg","Fe_Mg","C_Si","O_Si",
                        "Mg_Si","Ca_Si","Ti_Si","Fe_Si","C_O","Si_O","Mg_O","Ca_O",
                        "Ti_O","Fe_O"]
    else:
        plot_var = ["Fe","C","O","Na","Mg","Al","Si","Ca","Sc",
                        "Ti","V","Cr","Mn","Co","Ni","Y"]    
    hyp = ClassyReader("main.csv",delimiter=",")
    plotAgainst = hyp.Fe
    dict_one = {}
    dict_two = {}
    df1 = df1.rename_axis('star_name').reset_index()
    df2 = df2.rename_axis('star_name').reset_index()

    for zz, n in enumerate(plot_var):
        dict_one[n] = {"pred":[]}
        dict_two[n] = {"pred":[]}
        predFe_one = []
        predFe_two = []

        for zz, star in enumerate(hyp.star_name):
            if star in list(df1['star_name']):
                predFe_one.append(plotAgainst[zz])
                dict_one[n]["pred"].append(hyp.__getattribute__(n)[zz])
            if star in list(df2['star_name']):
                predFe_two.append(plotAgainst[zz])
                dict_two[n]["pred"].append(hyp.__getattribute__(n)[zz])
        print(len(predFe_one),len(predFe_two))
        left,width = 0.15,0.75
        bottom,height = 0.15,0.75
        rect_scatter = [left,bottom,width,height]
        axScatter = plt.axes(rect_scatter)
        axScatter.scatter(predFe_one,dict_one[n]["pred"],s=30,marker="o",linewidths=0.8,facecolor="None",
                      edgecolor="#D81B60",label="Shared Stars (≥90%) (1-6)")
        axScatter.scatter(predFe_two,dict_two[n]["pred"],s=30,marker="o",linewidths=0.8,facecolor="None",
                      edgecolor="#1E88E5",label="Shared Stars (≥90%) (7-11)")
        plt.title('Predicted Planet Hosts')

        if check == True:
            axScatter.set_ylabel(n.replace("_","/"),fontsize=15)
        else:
            if (n) == "Y":
                axScatter.set_ylabel("[Y/H]",fontsize=15)
            else:
                axScatter.set_ylabel("["+n+"/H]",fontsize=15)
        # If not [Fe/H] replace bottom line.
        axScatter.set_xlabel("[Fe/H]",fontsize=15)
        axScatter.legend(loc='upper left',scatterpoints=1,fontsize=8)
        plt.show()         
    
    return

def overplot_all():
    plot_values = ["Fe_Si"]
    hyp = ClassyReader("main.csv",delimiter=",")
    plotAgainst = hyp.Fe
    dict_one = {}
    dict_two = {}
    df1 = pd.read_csv("main.csv",usecols=["star_name"])
    df2 = pd.read_csv("big_overlap_experiment3.csv",usecols=["star_name"])

    for zz,n in enumerate(plot_values):
        dict_one[n]={"pred":[]}
        dict_two[n]={"pred":[]}
        predFe_one = []
        predFe_two = []

        for zz, star in enumerate(hyp.star_name):
            if star in list(df1['star_name']):
                predFe_one.append(plotAgainst[zz])
                dict_one[n]["pred"].append(hyp.__getattribute__(n)[zz])
            if star in list(df2['star_name']):
                predFe_two.append(plotAgainst[zz])
                dict_two[n]["pred"].append(hyp.__getattribute__(n)[zz])
                
        # Parameters for the bins in the x- and y-directions (which aren't equal)
        if (n) == "C_O":
            ybinl = 0.0
            ybinr = 1.0
        else:
            ybinl = 0.4
            ybinr = 2.0
        xbinl=-1.0
        xbinr=1.0
        binwidth=0.1
        binsx=np.arange(xbinl,xbinr+binwidth,binwidth)
        binsy=np.arange(ybinl,ybinr+binwidth,binwidth)

        # Stuff
        histPredFe_one = np.histogram(predFe_one,bins=binsx)
        normPredFe_one = []
        for num in histPredFe_one[0]:
            normPredFe_one.append(float(num)/float(max(histPredFe_one[0])))
        histPredFe_two = np.histogram(predFe_two,bins=binsx)
        normPredFe_two = []
        for num in histPredFe_two[0]:
            normPredFe_two.append(float(num)/float(max(histPredFe_two[0])))

        # Cleanup
        cleanpredE_one = [x for x in dict_one[n]['pred'] if str(x) != 'nan']
        cleanpredE_two = [x for x in dict_two[n]['pred'] if str(x) != 'nan']

        histPredE_one = np.histogram(cleanpredE_one,bins=binsy)
        normPredE_one = []
        for num in histPredE_one[0]:
            normPredE_one.append(float(num)/float(max(histPredE_one[0])))
        histPredE_two = np.histogram(cleanpredE_two,bins=binsy)
        normPredE_two = []
        for num in histPredE_two[0]:
            normPredE_two.append(float(num)/float(max(histPredE_two[0])))
            
        plt.clf()
        nullfmt=NullFormatter()

        # Scatter Plot Size
        left,width = 0.11,0.6
        bottom,height = 0.11,0.6
        bottom_h = left_h = left+width+0.05
        rect_scatter = [left,bottom,width,height]

        # Histogram stuff
        rect_histx = [left, bottom_h, width, 0.2]
        rect_histy = [left_h, bottom, 0.2, height]

        # Start with a rectangular figure
        plt.figure(1, figsize=(8,8))

        # Define the parameters/locations for the plotting        
        axScatter = plt.axes(rect_scatter)
        axHistx = plt.axes(rect_histx)
        axHisty = plt.axes(rect_histy)

        # no labels on the overlapping axes
        axHistx.xaxis.set_major_formatter(nullfmt)
        axHisty.yaxis.set_major_formatter(nullfmt)

        # Scatter Plot stuff
        axScatter.scatter(predFe_one,dict_one[n]["pred"],s=30,marker="o",linewidths=0.8,facecolor="None",
                      edgecolor="#D81B60",label="Full Star Dataset")
        axScatter.scatter(predFe_two,dict_two[n]["pred"],s=30,marker="o",linewidths=0.8,facecolor="None",
                      edgecolor="#1E88E5",label="Shared Stars (≥90%)")

        # Set the limits on the scatter plot.
        axScatter.set_xlim( [xbinl, xbinr] )
        axScatter.set_ylim( [ybinl, ybinr] )
    
        #Make the bar plots. Note that the horizontal one is barh.
        axHistx.bar(np.arange(xbinl, xbinr,binwidth),normPredFe_one,binwidth,facecolor="None", edgecolor="#D81B60", hatch='\\\\')
        axHisty.barh(np.arange(ybinl, ybinr,binwidth),normPredE_one,binwidth, facecolor="None",edgecolor="#D81B60", hatch='\\\\')

        axHistx.bar(np.arange(xbinl, xbinr,binwidth),normPredFe_two,binwidth,facecolor="None", edgecolor="#1E88E5", hatch='////')
        axHisty.barh(np.arange(ybinl, ybinr,binwidth),normPredE_two,binwidth, facecolor="None",edgecolor="#1E88E5", hatch='////')
    
        axHistx.set_xlim(axScatter.get_xlim())
        axHisty.set_ylim(axScatter.get_ylim())
        
        axHistx.set_title('Experiment 3',fontsize=10)
##        if n == 'Na':
##            plt.ylim(-1.5,1.5)
##            plt.xlim(-1,1)
##            axScatter.set_ylabel('[Na/H]')
##        elif (n == 'Si_O' or n == 'Mg_O'):
##            plt.ylim(0,0.25)
##            plt.xlim(-1,1)
##            axScatter.set_ylabel(n.replace("_","/"),fontsize=15)
##        else:
##            plt.ylim(0,2)
##            plt.xlim(-1,1)
##            axScatter.set_ylabel(n.replace("_","/"),fontsize=15)
##        # If not [Fe/H] replace bottom line.
        axScatter.set_ylabel(n.replace("_","/"),fontsize=15)
        axScatter.set_xlabel("[Fe/H]",fontsize=15)
        axScatter.legend(loc='best',scatterpoints=1,fontsize=8)        
        plt.show()

#plot_abundance(create_series(df, "planet_probabilities",False))
#plot_molar(create_series(df, "planet_probabilitiesmr", True))

##df_non_molar = create_series(df,"planet_probabilitiese1-set",'non-molar')
##df_molar = create_series(df, "planet_probabilitiese1mr",'molar')
##ensemble_comp(df_non_molar,df_molar,False)

#plot_abundance(create_series(df,"planet_probabilitiese1",'all'), False)
#plot_molar(create_series(df,"planet_probabilitiese1mr",True))
overplot_all()
