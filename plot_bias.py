import numpy as np
import os
import matplotlib.pyplot as plt
from planetpred.table_read import ClassyReader
from planetpred.simulation_final_nrh import working_dir
import pandas as pd

df = pd.read_csv("main.csv")

#print(df['discoverymethod'])
#print(df['pl_bmassj'])

count_transit = 0
count_radial = 0
count_imaging = 0
count_obm = 0

for discovery in df['discoverymethod']:
    if discovery == 'Transit':
        count_transit += 1
    elif discovery == 'Radial Velocity':
        count_radial += 1
    elif discovery == 'Imaging':
        count_imaging += 1
    elif discovery == 'Orbital Brightness Modulation':
        count_obm += 1
    else:
        continue

multi_one = 0
multi_two = 0
multi_three = 0
multi_four = 0
multi_five = 0

for multi in df['sy_pnum']:
    if multi == 1:
        multi_one += 1
    elif multi == 2:
        multi_two += 1
    elif multi == 3:
        multi_three += 1
    elif multi == 4:
        multi_four += 1
    elif multi == 5:
        multi_five += 1  
    else:
        continue

print(df['pl_orbper'])

#print(count_transit, count_radial, count_imaging, count_obm)

def plot_discovery_bias(count_transit, count_radial,
                        count_imaging, count_obm, title):
    columns = ('OBM','Imaging','Transit','RV')
    rows = [count_obm, count_imaging, count_transit, count_radial]

    plt.barh(columns,rows,color = 'royalblue',ec='black')
    plt.xlabel('Number of Planets')
    plt.ylabel('Discovery Method')
    plt.title(title)
    for i, v in enumerate(rows):
        plt.text(v, i, str(v))
    plt.show()

    return

def plot_mass_bias():
    mass_list = list()
    for i in range(len(df['pl_bmassj'])):
        if (df['pl_bmassj'][i]=='nan'):
            continue
        else:
            mass_list.append(df['pl_bmassj'][i])
    plt.hist(mass_list, color='royalblue', ec='black', bins=15)
    plt.xlabel('Planet Mass (M$_J$)')
    plt.ylabel('Number of Planets')
    plt.title('Mass Biases')
    plt.show()
    return

def plot_multi_bias(multi_five, multi_four,
                    multi_three, multi_two, multi_one,
                    title):
    columns = ('5','4','3','2','1')
    rows = [multi_five, multi_four, multi_three, multi_two, multi_one]

    plt.barh(columns,rows,color = 'royalblue',ec='black')
    plt.xlabel('Number of Systems')
    plt.ylabel('Number of Planets in System')
    plt.title(title)
    for i, v in enumerate(rows):
        plt.text(v, i, str(v))
    plt.show()
    return

def plot_period_bias():
    period_list = list()
    for i in range(len(df['pl_orbper'])):
        if (df['pl_orbper'][i]==float('nan')):
            continue
        else:
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


plot_discovery_bias(count_transit, count_radial,
                        count_imaging, count_obm, 'Discovery Method Biases')
plot_mass_bias()
plot_multi_bias(multi_five, multi_four,
                    multi_three, multi_two, multi_one,
                    'Multi Planet Systems')
plot_period_bias()
plot_radius_bias()
