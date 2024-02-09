import numpy as np
import os
import matplotlib.pyplot as plt
from planetpred.table_read import ClassyReader
from planetpred.simulation_final_nrh import working_dir
import pandas as pd
import yaml

#open csv
df = pd.read_csv("main.csv")

def plot_discovery_bias():
    discovery_methods = df['discoverymethod'].value_counts()
    discovery_methods = discovery_methods.rename(index={'Transit Timing Variations': 'TTV'})
    plt.barh(list(discovery_methods.index.values),list(discovery_methods),color = 'royalblue',ec='black')
    plt.xlabel('Number of Planets')
    plt.ylabel('Discovery Method')
    ##plt.title('Discovery Method Biases')
    plt.show()
    return

def plot_mass_bias():
    counts,edges,bars = plt.hist(list(df['pl_bmassj']), color='royalblue', ec='black', bins=15)
    plt.bar_label(bars)
    plt.xlabel('Planet Mass (M$_J$)')
    plt.ylabel('Number of Planets')
    ##plt.title('Mass Biases')
    plt.show()
    return

def plot_multi_bias():
    multi_planet = df['sy_pnum'].value_counts()
    plt.barh(list(multi_planet.index.values),list(multi_planet),color = 'royalblue',ec='black')
    plt.xlabel('Number of Systems')
    plt.ylabel('Number of Planets in System')
    ##plt.title('Multi Planet Systems')
    plt.show()
    return

def plot_period_bias():
    counts,edges,bars = plt.hist(list(df['pl_orbper']), color='royalblue',ec='black',bins=15)
    plt.bar_label(bars)
    plt.xlabel('Period (days)')
    plt.ylabel('Number of Planets')
    ##plt.title('Period Biases')
    plt.show()

def plot_radius_bias():
    counts,edges,bars = plt.hist(list(df['pl_rade']), color='royalblue',ec='black',bins=15)
    plt.bar_label(bars)
    plt.xlabel('Radius (R$_E$)')
    plt.ylabel('Number of Planets')
    ##plt.title('Radii Biases')
        
    plt.show()
    return

# Use .yaml file to get the elements for column.
def plot_element_bias():
    features = df.columns[2:19]
    keys = features
    dictionary = {}
    sorted_dict = {}

    for i in range(len(keys)):
        temp = df[features[i]].count()
        dictionary.update({keys[i]: temp})
    del dictionary['Li']

    sorted_keys = sorted(dictionary,key=dictionary.get)

    for w in sorted_keys:
        sorted_dict[w] = dictionary[w]

    elements = list(sorted_dict.keys())
    values = list(sorted_dict.values())
    plt.bar(elements,values,color = 'royalblue',ec='black')
    plt.xlabel('Number of stars')
    plt.ylabel('Elements')
    ##plt.title('Elements vs. Number of stars')
    plt.show()
    return

#plot_discovery_bias()
plot_mass_bias()
#plot_multi_bias()
#plot_period_bias()
#plot_radius_bias()
#plot_element_bias()

