# Made modication to code since it kept crashing on get_fscore:
# alg.booster().get_fscore() --> alg.get_booster().get_fscore()
#
# file, set number, golden set (T/F), plot X/Fe (T/F), save hyp plots (T/F)
#
# To run:
# import sys
# sys.argv = ["simulation_final_nrh.py","set_test", "False", "False", "True", "hypatia-nonCons-noThickDisk-planets-28Feb-nasa.csv"]
# execfile("simulation_final_nrh.py")
#
# Tutorial for XGBoost:
#  https://jessesw.com/XG-Boost/
#

import numpy as np
import yaml #
import pandas as pd #
import warnings
from datetime import datetime
from numpy import nan
import os

from sklearn import metrics
import xgboost as xgb #
from xgboost.sklearn import XGBClassifier


working_dir = os.path.dirname(os.path.realpath("__file__"))
#---------------- Definition---------------------------------------------

def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError

#-------------------------------------------------------------------------

def set_parameters(set_name, golden_set, input_file):
    
    
    golden = str_to_bool(golden_set)
    
    #-------------------------------------------------------------------------
    
    #read in the directory that is being run
    data_dir = set_name
    
    #read in the parameters file and load it

    full_path = os.path.join(working_dir,"{0}".format(data_dir),'params.yaml')
    stream = open(full_path, 'r')
    parameters = yaml.load(stream, Loader=yaml.FullLoader)
    
    #read in Hypatia data as pandas dataframe (2D structure), drop HIP numbers
    df  = pd.read_csv(input_file)
    
    set_number = set_name
    
    #-------------------------------------------------------------------------
    
    # Make a golden set if True. Then select 10 random confirmed exoplanet host stars as the golden.
    if golden:
        df2 = df.copy()
        df2.loc[df2[(df2['Exo']==1) & ((df2['pl_rade']>parameters['lower_planet_radius']) & (df2['pl_rade']<parameters['upper_planet_radius']))].sample(10, random_state=np.random.RandomState()).index,'Exo'] = 0
        yy = df2.loc[df2['Exo'] == 0].index
        zz = df.loc[df['Exo'] == 0].index
        changed = [ind for ind in yy if not ind in zz]
        changedhips = [df['star_name'][ind] for ind in changed]
        df = df2.copy()
        yy2 = df2.loc[df2['Exo'] == 0].index
        zz2 = df.loc[df['Exo'] == 0].index
        changed2 = [ind for ind in yy2 if not ind in zz2]
    #-------------------------------------------------------------------------
    
    df.index        = df['star_name']
    df['Exo']       = df['Exo'].astype('category') #category = limited possibilities
    df['sy_pnum']     = df['sy_pnum'].astype('category')
    df['pl_rade']  = df['pl_rade'].astype(np.number)
    df['Sampled']   = np.zeros((df.shape[0]))
    df['Predicted'] = np.zeros((df.shape[0]))
    df = df.drop(['star_name'], axis=1)
    
    # Print a bunch of stuff in terminal
    print('Parameters used in simulation:')
    print('------------------------------')
    print('')
    
    for key in parameters.keys():
        print('{0} = {1}'.format(key, parameters[key] ))
    
    cv_folds = parameters['cv_folds']
    early_stopping_rounds = parameters['early_stopping_rounds']
    N_iterations = parameters['N_iterations']
    N_samples = parameters['N_samples']
    upper_planet_radius = parameters['upper_planet_radius']
    lower_planet_radius = parameters['lower_planet_radius']
##    small_planet_radius = parameters['small_planet_radius']
    features = parameters['features']

    # Planet radius is not required. We do not want to drop those with no radius detected as it will remove all
    # entries with Exo = 0
    relevant_columns = features + ['Exo', 'Sampled', 'Predicted']    
    
    # Remove any entries with 'nan' values in the relevant_columns but keep the dataframe as is
    # The '*' arguement is an unpacking operator which allows us to use the individual elements in the
    # relevant_columns list as arguments for the dropna function
    if(parameters['dropnans']):
        df = df.dropna(subset=[*relevant_columns])
##        df=df.dropna(subset=['C', 'O', 'Na', 'Mg', 'Al', 'Si', 'Ca', 'Sc', 'Ti', 'V', 'Mn', 'Y', 'Exo', 'Sampled', 'Predicted'])
    
    print('Number of samples used in simulation: {0}'.format(df.shape[0]))
    
    print('')
    #Define the confusion matrix and other arrays
    cfm = np.zeros((2,2))
    
    auc_score_train       = []
    precision_score_train = []
    feat_imp_train        = pd.DataFrame(columns=features)
    probabilities_total   = pd.DataFrame(index=df.index)
    
    print('iteration \t estimators')
    print('---------------------------')
    
    #---------------------------XGBOOST LOOP----------------------------------------------

    # Loop for all of the iterations (defined in yaml)
    for iteration in range(0, N_iterations):

        #dataframe of 200 random hosts with small planets
        df_iter_with_exo = df[(df['Exo']==1) & ((df['pl_rade']>lower_planet_radius) & (df['pl_rade']<upper_planet_radius))].sample(N_samples, random_state=np.random.RandomState())

        #dataframe of 200 random non hosts
        df_iter_none_exo = df[df['Exo']==0].sample(N_samples, random_state=np.random.RandomState())
        
        # make a new dataframe of the 400 star subset
        df_train         = pd.concat([df_iter_with_exo, df_iter_none_exo], axis=0)
        # make a dataframe of those stars NOT in the training set (to predict on)
        df_predict       = df[~df.index.isin(df_train.index)]
        
        # The train dataframe with everything but the Exo column
        X = df_train.drop(['Exo'],axis=1)
        # The Exo column (and hips)
        Y = df_train.Exo
        
        # Note: Using gbtree booster
        alg = XGBClassifier(learning_rate =0.1, #def=0.3, prevents overfitting and makes feature weight conservative, def=0.1 for 2019 paper
                            n_estimators=1000, #number of boosted trees to fit, def=1000 for 2019 paper
                            max_depth=6, #def=6, max depth of tree/complexity
                            min_child_weight=1, #def=1, min weight needed to continue leaf partitioning
                            gamma=1, #def=0, minimum loss reduction required to make partition on a leaf
                            subsample=0.8, #def=1, subsample ratio of the training set
                            colsample_bytree=0.8, #def=1, subsample ratio of columns when making each tree
                            objective= 'binary:logistic', #def=linear, logistic regression for binary classification, output probability
                            nthread=8, #original = 8, but issue on laptop...def=max, number of parallel threads used to run xgboost
                            scale_pos_weight=1, #def=1, balance positive and neg weights
                            seed=27,  #def=0, random number seed
                            eval_metric='auc') # To prevent deprecation warning use here
                            
        #get input parameters of algorithm
        xgb_param = alg.get_xgb_params()
        
        #construct training set matrix
        xgtrain = xgb.DMatrix(X[features].values, label=Y)
        
        #cross validation (CV) of xgboost to avoid overfitting
        cvresult = xgb.cv(xgb_param, xgtrain, num_boost_round=alg.get_params()['n_estimators'], nfold=cv_folds, metrics='auc', early_stopping_rounds=early_stopping_rounds)
        
        alg.set_params(n_estimators=cvresult.shape[0])
        print(iteration, '\t \t', cvresult.shape[0])
        
##        alg.fit(X[features], Y, eval_metric='auc')
        alg.fit(X[features],Y)
    
        dtrain_predictions = alg.predict(X[features])
        dtrain_predprob    = alg.predict_proba(X[features])[:,1]
        
        feat_imp        = alg.get_booster().get_fscore()
        # See how the algorithm performs on the Exo data
        auc_score       = metrics.roc_auc_score(    Y, dtrain_predprob)
        precision_score = metrics.precision_score(  Y, dtrain_predictions)
        metric_score    = metrics.confusion_matrix( Y, dtrain_predictions)
        
        # Weighting function to ignore the null values
        normalized_features = pd.DataFrame((1 - df_train[features].isnull().sum()/df_train[features].count())* pd.Series(alg.get_booster().get_fscore()), columns=[iteration]).T
        
        #calculate the confusion matrix
        feat_imp_train = pd.concat([feat_imp_train, pd.DataFrame(feat_imp, columns=features, index=[iteration])])
        feat_imp_train_normal = pd.concat([feat_imp_train, normalized_features])
        auc_score_train.append(auc_score)
        precision_score_train.append(precision_score)
        cfm += metric_score

        # 2MASS I is a duplicated index in the main.csv sheet
        # Array lengths not matching up
        df.loc[df_predict.index, 'Sampled']   += np.ones(len(df_predict.index))
        df.loc[df_predict.index, 'Predicted'] += alg.predict(df_predict[features])
        df.loc[df_predict.index, 'Prob']       = alg.predict(df_predict[features])
        
        values = df['Prob']
        probabilities_total = pd.concat([probabilities_total, pd.Series(values, name=str(iteration))], axis=1)
    
        if(not iteration % 10):
            probabilities_total.to_pickle('{0}/probabilities_total.pkl'.format(data_dir))
    
    
    #-------------------------------------------------------------------------
    
    # Calculate the confusion matrix
    cfm /= N_iterations
    cfm[0] /= cfm[0].sum()
    cfm[1] /= cfm[1].sum()
    
    # Print confusion matrix
    print(np.round(cfm, 3))
    df['Prob'] = df['Predicted'] / df['Sampled']
    
    ###########-------------------Output List of Planets------------------------#########
    
    #Find the stars with >90% probability of hosting a planet, with the Sampled, Predicted, and Prob columns
    planets = df[(df.Prob>.90) & (df.Exo==0)][['Sampled', 'Predicted', 'Prob']]
    print('Number of most probable planet hosts: {0}'.format(planets.shape[0]))
    
    #Sort the stars with predicted planets and save that file
    planetprobs = planets.sort_values(by='Prob', ascending=False)
    name = data_dir+'/figures/planet_probabilities'+str(datetime.today().strftime('-%h%d-%H%M'))+'.csv'
    #name = data_dir+'/figures/planet_probabilities.csv'
    outfile = open(name, 'w')
    planetprobs.to_csv(outfile)
    outfile.close()
    
    #Create a second list with all stars in Hypatia and the probabilities
    planets2 = df[(df.Prob>.0) & (df.Exo==0)][['Sampled', 'Predicted', 'Prob']]
    if golden: #if 10 stars were randomly taken out
        changeddf = pd.DataFrame([]) #make empty dataframe
        for star in changedhips:  #loop over the 10 known planets hosts (defined at top)
##            changeddf = changeddf.append(planets2.loc[planets2.index==star])
            pd.concat([changeddf,planets2.loc[planets2.index==star]])
            if planets2.loc[planets2.index==star].empty: #catch for when a known planet host was cut (bc of abunds)
                temp = pd.Series([nan,nan,nan], index=['Sampled', 'Predicted', 'Prob'])
                temp.name = star
##                changeddf = changeddf.append(temp) #append blank file (with star name as index)
                pd.concat([changeddf,temp])
        #Save golden set as a separate file with the date and time as a tag
        filename ='{0}/figures/goldenSetProbabilities'+str(datetime.today().strftime('-%h%d-%H%M'))+'.csv'
        changeddf.to_csv(filename.format(set_number), na_rep=" ")
    
    #Save the file with all of the probabilities
    planetprobs2 = planets2.sort_values(by='Prob', ascending=False)
    name2 = data_dir+'/figures/planet_probabilitiesAll'+str(datetime.today().strftime('-%h%d-%H%M'))+'.csv'
    #name2 = data_dir+'/figures/planet_probabilitiesAll.csv'
    outfile2 = open(name2, 'w')
    planetprobs2.to_csv(outfile2)
    outfile2.close()
    
    ###########------------------------Save Files------------------------##########
    print('Saving data files')
    
    #Save files
    feat_imp_train.to_pickle('{0}/features_train.pkl'.format(data_dir))
    feat_imp_train_normal.to_pickle('{0}/features_train_normal.pkl'.format(data_dir))
    probabilities_total.to_pickle('{0}/probabilities_total.pkl'.format(data_dir))
    df.to_pickle('{0}/df_info_all.pkl'.format(data_dir))
    
    np.save('{0}/auc_score_train.npy'.format(data_dir), np.array(auc_score_train))
    np.save('{0}/precision_score_train.npy'.format(data_dir), np.array(precision_score_train))
    np.save('{0}/cfm.npy'.format(data_dir), cfm)
    
    print('Simulation completed successfully.')
    if golden:
        print("Changed indices and star_names numbers:")
        print(changed)
        print(changedhips)
    

