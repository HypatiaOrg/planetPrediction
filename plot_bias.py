import numpy as np
import os
import matplotlib.pyplot as plt
from planetpred.table_read import ClassyReader
from planetpred.simulation_final_nrh import working_dir
import pandas as pd

df = pd.read_csv("main.csv")

#print(count_transit, count_radial, count_imaging, count_obm)

def plot_discovery_bias():
    columns = ('OBM','Imaging','Transit','RV')
    rows = [df['discoverymethod'].value_counts()[3],
            df['discoverymethod'].value_counts()[2],
            df['discoverymethod'].value_counts()[1],
            df['discoverymethod'].value_counts()[0]]

    plt.barh(columns,rows,color = 'royalblue',ec='black')
    plt.xlabel('Number of Planets')
    plt.ylabel('Discovery Method')
    plt.title('Discovery Method Biases')
    for i, v in enumerate(rows):
        plt.text(v, i, str(v))
    plt.show()

    return

def plot_mass_bias():
    mass_list = list()
    for i in range(len(df['pl_bmassj'])):
        mass_list.append(df['pl_bmassj'][i])
    plt.hist(mass_list, color='royalblue', ec='black', bins=15)
    plt.xlabel('Planet Mass (M$_J$)')
    plt.ylabel('Number of Planets')
    plt.title('Mass Biases')
    plt.show()
    return

def plot_multi_bias():
    columns = ('5','4','3','2','1')
    rows = [df['sy_pnum'].value_counts()[5],
            df['sy_pnum'].value_counts()[4],
            df['sy_pnum'].value_counts()[3],
            df['sy_pnum'].value_counts()[2],
            df['sy_pnum'].value_counts()[1]]

    plt.barh(columns,rows,color = 'royalblue',ec='black')
    plt.xlabel('Number of Systems')
    plt.ylabel('Number of Planets in System')
    plt.title('Multi Planet Systems')
    for i, v in enumerate(rows):
        plt.text(v, i, str(v))
    plt.show()
    return

def plot_period_bias():
    period_list = list()
    for i in range(len(df['pl_orbper'])):
        period_list.append(df['pl_orbper'][i])
    plt.hist(period_list, color='royalblue',ec='black',bins=100)
    plt.xlabel('Period (days)')
    plt.ylabel('Number of Planets')
    plt.title('Period Biases')
    plt.show()

def plot_radius_bias():
    radius_list = list()
    for i in range(len(df['pl_radj'])):
        if (df['pl_radj'][i]==float('nan')):
            continue
        else:
            radius_list.append(df['pl_radj'][i])
    plt.hist(radius_list, color='royalblue',ec='black',bins=20)
    plt.xlabel('Radius (R$_J$)')
    plt.ylabel('Number of Planets')
    plt.title('Radii Biases')
    plt.show()
    return

def plot_element_bias():
    columns = ('Fe','C','O','Na', 'Mg', 'Al', 'Si', 'Ca', 'Sc',
               'Ti','V','Cr','Mn','Co','Ni','Y')
    rows = [df['Fe'].count(), df['C'].count(), df['O'].count(),
            df['Na'].count(), df['Mg'].count(), df['Al'].count(),
            df['Si'].count(), df['Ca'].count(), df['Sc'].count(),
            df['Ti'].count(), df['V'].count(), df['Cr'].count(),
            df['Mn'].count(), df['Co'].count(), df['Ni'].count(),
            df['Y'].count()]

    plt.barh(columns,rows,color = 'royalblue',ec='black')
    plt.xlabel('Number of stars')
    plt.ylabel('Elements')
    plt.title('Elements vs. Number of stars')
    for i, v in enumerate(rows):
        plt.text(v, i, str(v))
    plt.show()
    return

plot_discovery_bias()
plot_mass_bias()
plot_multi_bias()
plot_period_bias()
plot_radius_bias()
plot_element_bias()

