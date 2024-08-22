import sys
import os
sys.path.append(os.path.dirname(os.path.realpath("__file__")))
from planetpred.simulation_final_nrh import set_parameters
from planetpred.simulation_plots import plot_parameters
from planetpred.simulation_hyp_plots import hyp_plot_parameters
from planetpred.total_prob import process_probabilities

'''
Description of keywords:
setname = Which folder and yaml file are being run on
goldenYN = Whether to separate a golden set to be tested on
XFeYN = Whether to plot [X/Fe] (True) or [X/H] (False)
plotYN = Whether to save plots (True) or not (False)
input_file_name = File that has abundances and whether a star is an exoplanet host star
'''

#file_name = "simulation_final_nrh.py"
experiment_name = 'experiment-3\\'
setname = "set7"
molar_ratio = True
goldenYN = "True"
XFeYN = "True"
plotYN = "True"
input_file_name = "main.csv"

for i in range(25): #Unique standalone trees that have nothing to do with each other
    set_parameters(set_name=experiment_name+setname, golden_set=goldenYN, input_file=input_file_name)
    plot_parameters(set_name=experiment_name+setname)
##    hyp_plot_parameters(set_name=setname, plotXFe=XFeYN, saveplot=plotYN)
# Plot the predicted planet hosts after the main loop runs.
# While molar ratio plotting is figured out, plot any ensemble that does not
# use molar ratios otherwise ignore.
if molar_ratio:
    print("Skipping hyp_plot_parameters.")
else:
    hyp_plot_parameters(set_name=experiment_name+setname, plotXFe=XFeYN, saveplot=plotYN)
