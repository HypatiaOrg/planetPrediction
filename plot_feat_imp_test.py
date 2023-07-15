import numpy as np
import pandas as pd
import yaml
import seaborn
import matplotlib.pyplot as plt

## ------Import the Data-----------------------------------------

set_name = "Experiment 3/set7-null"
stream = open('{0}/params.yaml'.format(set_name), 'r')
parameters = yaml.load(stream, Loader=yaml.FullLoader)
features = parameters['features']

df = pd.read_csv('main.csv')
results = pd.read_pickle('{0}/df_info_all.pkl'.format(set_name))

data = pd.read_pickle('{0}/features_train.pkl'.format(set_name))
finite_count = df[features].count() / df[features].count().max()
normalized = finite_count*data

# These are the values for the feature importance and errors
# After being normalized
feat_imp = normalized.mean()
error    = normalized.sem()

error /= feat_imp.max()
feat_imp /= feat_imp.max()


## -----Visualize the Data---------------------------------------

print(feat_imp)
print(error)

# Merge Feature Importance and Errors
fa = pd.concat([feat_imp,error],axis=1)

# Sort the pandas array by the feature importance
sa = fa.sort_values(by=0)

print(sa)
##input()

for i in range(0,len(sa)):
    sa.index.values[i] = sa.index.values[i].replace('_','/')

# Create the plot
fig, ax = plt.subplots()
hbars = ax.barh(sa.index.values,
                sa[0], xerr=sa[1],
                edgecolor="black",capsize=4)
ax.set_xlabel('Weighted Feature Importance Score')
ax.set_ylabel('Feature')
ax.set_title('Feature Importance')

###Verify if the errors are being plotted correctly
##ax.bar_label(hbars, labels=['±%.4f' % e for e in sa[1]],
##             padding=8, color='black', fontsize=8)
#Print to screen
plt.show()

## -----End---------------------------------------
