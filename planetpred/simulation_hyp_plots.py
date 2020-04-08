#
# Run from the main hypatia/ directory.
# Remember to change which set it is being run out of.

import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
from scipy.stats import ks_2samp
from planetpred.table_read import ClassyReader
from datetime import datetime
#from matplotlib import rc
from planetpred.simulation_final_nrh import working_dir

#rc('text', usetex=True)  #for LaTeX to make the plots look good
plt.style.use('ggplot')  #'default'
plt.rcParams['axes.facecolor']='whitesmoke'

#---------------- Definition---------------------------------------------

def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError

#------------------------Inputs-----------------------------------------


def hyp_plot_parameters(set_name, plotXFe, saveplot):
    
    #------------------------Input Changes-----------------------------------------
    
    
    if (set_name=="set5"):
        elements = ['Na', 'Mg', 'Al', 'Si', 'Ca', 'Sc', 'Ti', 'V',  'Cr', 'Mn', 'Co', 'Ni', 'Y1']
    elif set_name=="set4":
        elements = ['C', 'O', 'Na', 'Mg', 'Al', 'Si', 'Ca', 'Sc', 'Ti', 'V', 'Mn', 'Y1', 'Fe']
    elif (set_name=="set3"):
        elements = ['Na', 'Mg', 'Al', 'Si', 'Ca', 'Sc', 'Ti', 'V',  'Cr', 'Mn', 'Co', 'Ni', 'Y1', 'Fe']
    elif set_name=="set2":
        elements = ['Na', 'Mg', 'Al', 'Si', 'Ca', 'Sc', 'Ti', 'V',  'Cr', 'Mn', 'Co', 'Ni', 'Y1', 'C', 'O']
    elif set_name=="set1":
        elements = ['Na', 'Mg', 'Al', 'Si', 'Ca', 'Sc', 'Ti', 'V',  'Cr', 'Mn', 'Co', 'Ni', 'Y1', 'C', 'O', 'Fe']
    elif set_name=="set6":
        elements = ['C', 'O', 'Fe']
    else:
        raise TypeError("The set name you listed doesn't have elements associated with it.")

    
    
    if plotXFe:
        xbinl = -1.0
        xbinr = 0.7
        ybinl = -0.7
        ybinr = 0.9
    else:
        xbinl = -1.0
        xbinr = 0.7
        ybinl = -0.9
        ybinr = 0.9
    
    #--------------------------------Running the Numbers---------------------------------
    
    hyp = ClassyReader("hypatia-nonCons-noThickDisk-planets-28Feb-nasa.csv", delimiter=",")
    predicted = ClassyReader(set_name+"/figures/planet_probabilities_big.csv", delimiter=",")

    element_dict = {}
    for zz, n in enumerate(elements):
        print(n)
        element_dict[n] = {"pred": [], "exo": [], "other": []}
        # temp1 = "pred"+n
        # temp2 = "exo"+n
        # temp3 = "other"+n
    
    
    #Find the abundances for the star, based on whether it's a predicted exoplanet host
    # star, an actual planet host star, or neither. Then, depending on whether or not
    # [X/Fe] is to be plotted, calculate the abundance.


        # vars()[temp1] = []
        # vars()[temp2] = []
        # vars()[temp3] = []

        predFe = []
        exoFe = []
        otherFe = []

        for zz, star in enumerate(hyp.HIP):
            if star in predicted.HIP:
                predFe.append(hyp.Fe[zz])
                if plotXFe:
                    # vars()[temp1].append(hyp[n][zz]-hyp.Fe[zz])
                    element_dict[n]["pred"].append(hyp.__getattribute__(n)[zz]-hyp.Fe[zz])
                else:
                    # vtars()[temp1].append(hyp[n][zz])
                    element_dict[n]["pred"].append(hyp.__getattribute__(n)[zz])
            elif hyp.Exo[zz]==1:
                exoFe.append(hyp.Fe[zz])
                if plotXFe:
                    # vars()[temp2].append(hyp[n][zz]-hyp.Fe[zz])
                    element_dict[n]["exo"].append(hyp.__getattribute__(n)[zz] - hyp.Fe[zz])
                else:
                    # vars()[temp2].append(hyp[n][zz])
                    element_dict[n]["exo"].append(hyp.__getattribute__(n)[zz])
            else:
                otherFe.append(hyp.Fe[zz])
                if plotXFe:
                    # vars()[temp3].append(hyp[n][zz]-hyp.Fe[zz])
                    element_dict[n]["other"].append(hyp.__getattribute__(n)[zz] - hyp.Fe[zz])
                else:
                    # vars()[temp3].append(hyp[n][zz])
                    element_dict[n]["other"].append(hyp.__getattribute__(n)[zz])
    
    # Parameters for the bins in the x- and y-directions (which aren't equal)
        binwidth = 0.1
        binsx = np.arange(xbinl, xbinr + binwidth, binwidth)
        binsy = np.arange(ybinl, ybinr + binwidth, binwidth)
    
    
    # Python's histogram has no way to normalize the maximum bin to == 1, so
    # first you have to calculate the histogram, take the first element of
    # that object (which shows the count, the second element has the bins)
    # and normalize the bins so the max is 1.
    
    # Commented out in case a plot with non-FeH on the x-axis needs to be made (and cleaned)
    #   cleanpredFe = [x for x in predFe if str(x) != 'nan']
    #   cleanexoFe = [x for x in exoFe if str(x) != 'nan']
    #   cleanotherFe = [x for x in otherFe if str(x) != 'nan']
    
        histOthFe = np.histogram(otherFe,bins=binsx)
        normOthFe = []
        for num in histOthFe[0]:
            normOthFe.append(float(num)/float(max(histOthFe[0])))
    
        histExoFe = np.histogram(exoFe,bins=binsx)
        normExoFe = []
        for num in histExoFe[0]:
            normExoFe.append(float(num)/float(max(histExoFe[0])))
    
        histPredFe = np.histogram(predFe,bins=binsx)
        normPredFe = []
        for num in histPredFe[0]:
            normPredFe.append(float(num)/float(max(histPredFe[0])))
    
    # There are nans in the X/Fe or X/H distributions so they need to be removed.
    # To add it to the overarching dictionary, do:
    # element_dict[n]['cleanpredE'] = [x for x in element_dict[n]['pred'] if str(x) != 'nan']
        cleanpredE = [x for x in element_dict[n]['pred'] if str(x) != 'nan']
        cleanexoE = [x for x in element_dict[n]['exo'] if str(x) != 'nan']
        cleanotherE = [x for x in element_dict[n]['other'] if str(x) != 'nan']
    
        print("raw kstest", ks_2samp(element_dict[n]["pred"], element_dict[n]["exo"])[1])
        print("cleankstest", ks_2samp(cleanpredE, cleanexoE)[1])
    
    # Same as above to calculate the max bin == 1.
        histOthE = np.histogram(cleanotherE,bins=binsy)
        normOthE = []
        for num in histOthE[0]:
            normOthE.append(float(num)/float(max(histOthE[0])))
    
        histExoE = np.histogram(cleanexoE,bins=binsy)
        normExoE = []
        for num in histExoE[0]:
            normExoE.append(float(num)/float(max(histExoE[0])))
    
        histPredE = np.histogram(cleanpredE,bins=binsy)
        normPredE = []
        for num in histPredE[0]:
            normPredE.append(float(num)/float(max(histPredE[0])))
    
    #Star the process for plotting.
        plt.clf()
        nullfmt   = NullFormatter()
    
    # definitions for the axes
        left, width = 0.11, 0.65
        bottom, height = 0.11, 0.65
        bottom_h = left_h = left+width+0.02
    
        rect_scatter = [left, bottom, width, height]
        rect_histx = [left, bottom_h, width, 0.2]
        rect_histy = [left_h, bottom, 0.2, height]
    
    # start with a rectangular Figure
        plt.figure(1, figsize=(8,8))
    
    # Define the parameters/locations for the plotting.
        axScatter = plt.axes(rect_scatter)
        axHistx = plt.axes(rect_histx)
        axHisty = plt.axes(rect_histy)
    
    # no labels on the overlapping axes
        axHistx.xaxis.set_major_formatter(nullfmt)
        axHisty.yaxis.set_major_formatter(nullfmt)
    
    #Make the scatter plot.
        axScatter.scatter(otherFe, element_dict[n]["other"], s=60,facecolor="None",edgecolor="salmon", label='Stars Less Likely to Host ($<$90$\%$)')
        axScatter.scatter(exoFe,element_dict[n]["exo"],s=60,facecolor="None",edgecolor="navy", label='Known Planet Hosts')
        axScatter.scatter(predFe,element_dict[n]["pred"],s=30,marker="D",linewidths=0.5,facecolor="None",edgecolor="#1b9e77", label='Predicted Planet Hosts ($<$90$\%$)')
        # Note that Predicted Planet is \ge but LaTeX is needed

    # Set the limits on the scatter plot.
        axScatter.set_xlim( [xbinl, xbinr] )
        axScatter.set_ylim( [ybinl, ybinr] )
    
    #Make the bar plots. Note that the horizontal one is barh.
        axHistx.bar(np.arange(xbinl, xbinr,binwidth),normOthFe,binwidth,color="salmon")
        axHistx.bar(np.arange(xbinl, xbinr,binwidth),normExoFe,binwidth,facecolor="None", edgecolor="navy", hatch='\\', linewidth=1)
        axHistx.bar(np.arange(xbinl, xbinr,binwidth),normPredFe,binwidth,facecolor="None", edgecolor="#1b9e77", hatch='////')
    
        axHisty.barh(np.arange(ybinl, ybinr,binwidth),normOthE,binwidth, color="salmon")
        axHisty.barh(np.arange(ybinl, ybinr,binwidth),normExoE,binwidth, facecolor="None",edgecolor="navy", hatch='\\', linewidth=1)
        axHisty.barh(np.arange(ybinl, ybinr,binwidth),normPredE,binwidth, facecolor="None",edgecolor="#1b9e77", hatch='////')
    
        axHistx.set_xlim(axScatter.get_xlim())
        axHisty.set_ylim(axScatter.get_ylim())
    
    # Adapt the labeling based on what's being plotted.
        axScatter.set_xlabel("[Fe/H]", fontsize=15)
    
        if plotXFe:
            if n=="Y1":
                axScatter.set_ylabel("[Y/Fe]", fontsize=15)
            else:
                axScatter.set_ylabel("["+n+"/Fe]", fontsize=15)
        else:
            if n=="Y1":
                axScatter.set_ylabel("[Y/H]", fontsize=15)
            else:
                axScatter.set_ylabel("["+n+"/H]", fontsize=15)
    
        axHistx.set_ylabel("Relative Dist", fontsize=12)
        axHisty.set_xlabel("Relative Dist", fontsize=12)
    
    #Leftover from the initial debugging
        #axHistx.set_xlim([xbinl, xbinr])
        #axHisty.set_ylim([-0.6,0.9])
    
    #    plt.setp(ax_marg_x.get_xticklabels(), visible=False)
    #    plt.setp(ax_marg_y.get_yticklabels(), visible=False)
    #
    #    ax_joint.set_xlabel("[Fe/H]")
    #    ax_joint.set_ylabel("["+n+"/Fe]")
    #
    #    # Set labels on marginals
    #    ax_marg_y.set_xlabel('Marginal x label')
    #    ax_marg_x.set_ylabel('Marginal y label')
    #
    #    plt.ylim([-1.0,0.8])
    #    plt.xlim([xbinl, xbinr])
    #    #plt.xlabel("[Fe/H]")
    #    #plt.ylabel("["+n+"/Fe]")
        if (n=="Mn" or not plotXFe):
            axScatter.legend(loc='upper left', scatterpoints=1,fontsize=8)
        else:
            axScatter.legend(loc='lower left', scatterpoints=1,fontsize=8)
    
        if saveplot:
            full_plot_dir = os.path.join(working_dir, set_name, 'figures')
            if not os.path.isdir(full_plot_dir):
                os.mkdir(full_plot_dir)
            if plotXFe:
                plt.savefig(os.path.join(full_plot_dir, "predicted"+n+"Fe"+str(datetime.today().strftime('-%h%d-%H%M'))+".pdf")) #note only pdf will show the cross-hatching
            else:
                plt.savefig(os.path.join(full_plot_dir, "predicted"+n+"H-"+str(datetime.today().strftime('-%h%d-%H%M'))+".pdf"))
        else:
            plt.show()
    
    
    
    # Make sure that there are no known hosts in the predicted hosts: aa == 0
    #aa = []
    #for ii in range(len(hyp)):
    #    for star in predicted.HIP:
    #        if hyp.HIP[ii]==star:
    #            aa.append(hyp.Exo[ii])
