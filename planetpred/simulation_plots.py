import numpy as np
import os
import yaml
import pandas as pd
from datetime import datetime


import matplotlib.pyplot as plt
from planetpred.simulation_final_nrh import working_dir
# from sklearn.model_selection import GridSearchCV


plt.style.use('ggplot')


def plot_parameters(set_name):
    
    stream = open('{0}/params.yaml'.format(set_name), 'r')
    parameters = yaml.load(stream, Loader=yaml.FullLoader)
    features = parameters['features']
    
    df = pd.read_csv('hypatia-nonCons-noThickDisk-planets-28Feb-nasa.csv')
    results = pd.read_pickle('{0}/df_info_all.pkl'.format(set_name))
    
    data = pd.read_pickle('{0}/features_train.pkl'.format(set_name))
    finite_count = df[features].count() / df[features].count().max()
    normalized = finite_count*data
    
    feat_imp = normalized.mean()
    error    = normalized.sem()
    
    error /= feat_imp.max()
    feat_imp /= feat_imp.max()
    #feat_imp.sort_values().plot(kind='barh', xerr=error)
    
    ###########-------------------Feature Importance---------------#########
    plt.clf()
    feat_imp.sort_values().plot(kind='barh', xerr=error, color="steelblue")
    plt.xlabel('Weighted Feature Importance Score')
    plt.grid(True, alpha=0.8)
    #plt.title("Vol+Litho+Fe")
    plt.rc('xtick', labelsize=14)
    plt.rc('ytick', labelsize=14)
    full_file_dir = os.path.join(working_dir, set_name, "figures")
    if not os.path.exists(full_file_dir):
        os.mkdir(full_file_dir)

    filename = os.path.join(full_file_dir, 'Feature_importance'+str(datetime.today().strftime('-%h%d-%H%M'))+'.pdf')
    print(filename)
    plt.savefig(filename)
    
    cfm = np.load(os.path.join(working_dir, set_name, 'cfm.npy'))
    print(cfm)
    print('')
    print(feat_imp)
    
    
    ###########-------------------Number of Nulls------------------------#########
    plt.clf()
    df[features].isnull().sum().sort_values(ascending=True).plot(kind='barh')
    plt.grid(True, alpha=0.8)
    plt.xlabel('Number of null values in dataset')
    filename2 = os.path.join(full_file_dir, 'NumberNulls'+str(datetime.today().strftime('-%h%d-%H%M'))+'.pdf')
    plt.savefig(filename2)


