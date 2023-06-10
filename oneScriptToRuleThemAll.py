import sys
import os
sys.path.append(os.path.dirname(os.path.realpath("__file__")))


from planetpred.simulation_final_nrh import set_parameters
from planetpred.simulation_plots import plot_parameters
from planetpred.simulation_hyp_plots import hyp_plot_parameters

'''
Description of keywords:
setname = Which folder and yaml file are being run on
goldenYN = Whether to separate a golden set to be tested on
XFeYN = Whether to plot [X/Fe] (True) or [X/H] (False)
plotYN = Whether to save plots (True) or not (False)
input_file_name = File that has abundances and whether a star is an exoplanet host star
'''

#file_name = "simulation_final_nrh.py"
setname = "set5"
goldenYN = "True"
XFeYN = "True"
plotYN = "True"
input_file_name = "main.csv"

for i in range(25): #Unique standalone trees that have nothing to do with each other
    set_parameters(set_name=setname, golden_set=goldenYN, input_file=input_file_name)
    plot_parameters(set_name=setname)
##    hyp_plot_parameters(set_name=setname, plotXFe=XFeYN, saveplot=plotYN)

# Plot the predicted planet hosts after the main loop runs.
# New setup loops through all files after they are produced.
hyp_plot_parameters(set_name=setname, plotXFe=XFeYN, saveplot=plotYN)
print("Save the last planet_probabilities lists as _big and run simulation_hyp_plots")


