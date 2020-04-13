# planetPrediction
Code to accompany the paper "A Recommendation Algorithm to Predict Giant Exoplanet Host Stars Using Stellar Abundances" by Hinkel et al. (2019). Packages needed:
"numpy", "pandas", "PyYaml", "xgboost", "matplotlib", "scipy", "sklearn"

The main code is simulation_final_nrh, which pulls data from hypatia-nonCons-noThickDisk-planets-28Feb-nasa file, a file that I put together from combining Hypatia data and info from the NASA Exoplanet Archive. The simulation uses the yaml file in the set1 directory (where set1 is the Vol+Litho+Sidero+Fe ensemble). If you want the general feature importance score plots or information on nulls in the data, that is done by calling simulation_plots. If you want comparisons with Hypatia data (i.e. from the hypatia-nonCons file), then you first run the simulation_final file one or many times (I did it hundreds of times), create a planet_probabilities_big file, then run simulation_hyp_plots. One example of planet_probabilities_big is included in set1. Also, the hypatia-nonCons file should be updated with the most recent Hypatia data. 

Everything is run from oneScriptToRuleThemAll, which sets up which set you want to run and toggles other options. Included here is one set or ensemble as an example, where the other sets would be:

Set1 = Volatiles + Lithophiles + Siderophile + Fe: C, O, Na, Mg, Al, Si, Ca, Sc, Ti, V, Mn, Y, Cr, Co, Ni, Fe (16)

Set2 = Volatiles + Lithophiles + Siderophile: C, O, Na, Mg, Al, Si, Ca, Sc, Ti, V, Mn, Y, Cr, Co, Ni (15)

Set3 = Lithophiles + Siderophile + Fe: Na, Mg, Al, Si, Ca, Sc, Ti, V, Mn, Y, Cr, Co, Ni, Fe (14)

Set4 = Volatiles + Lithophiles + Fe: C, O, Na, Mg, Al, Si, Ca, Sc, Ti, V, Mn, Y, Fe (13)

Set5 = Lithophiles + Siderophile: Na, Mg, Al, Si, Ca, Sc, Ti, V, Mn, Y, Cr, Co, Ni (13)

Set6 = C, O, Fe (3, not listed in the paper) 

per [Hinkel et al. (2019).](https://ui.adsabs.harvard.edu/abs/2019ApJ...880...49H/abstract)

After oneScript is run, a new folder called "figures" will be created in the set folder. This folder is where the algorithm output is saved, such as the plots (if plotYN = True), the planet predictional probability files, golden set probabilities (if goldenYN = True), and the feature importance plots. The files are day and/or time stamped to accumulate the larger statistics over many, many runs.

As an aside, simulation_hyp_plots is admittedly a bit hacked. I've since created a much nicer plotting definition to create the stacked scatter-hist-hist plots, but I decided not to delay getting the code online to test and debug. If you'd like the cleaner plotting code, feel free to shoot me an email. 
