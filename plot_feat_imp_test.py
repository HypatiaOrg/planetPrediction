import numpy as np
import pandas as pd
import yaml
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from xgboost import XGBRegressor

## ------Import the Data-----------------------------------------
molar = True
set_name = "Experiment 3/setm10-super"
stream = open('{0}/params.yaml'.format(set_name), 'r')
parameters = yaml.load(stream, Loader=yaml.FullLoader)
features = parameters['features']

df = pd.read_csv('main.csv')
results = pd.read_pickle('{0}/df_info_all.pkl'.format(set_name))

data = pd.read_pickle('{0}/features_train.pkl'.format(set_name))

if data.columns[0].__contains__('/'):
    data.columns = [col.replace('/','_') for col in data.columns]

##for i in range(len(data.columns)):
##    if str(data.columns[i]).__contains__('/'):
##        str(data.columns).replace('/','_')

finite_count = df[features].count() / df[features].count().max()
normalized = finite_count*data

# These are the values for the feature importance and errors
# After being normalized
feat_imp = normalized.mean()
error    = normalized.sem()

error /= feat_imp.max()
feat_imp /= feat_imp.max()

## ------Switch Statement - Colors---------------------

def switch(set_name):

    # Hex Color Code: Color Blindness
    # https://davidmathlogic.com/colorblind/#%23D81B60-%231E88E5-%23FFC107-%23004D40
    no_variation = '#1E88E5'
    variation_one = '#D81B60'
    variation_two = '#FFC107'
    variation_three = '#004D40'
    variation_four = '#EF7697'
    variation_five = '#EF36F9'

    # Hatch Style Reference:
    # https://matplotlib.org/stable/gallery/shapes_and_collections/hatch_style_reference.html
    pattern_one = '//'
    pattern_two = '..'
    pattern_three = 'xx'
    pattern_four = 'oo'

    ## -----Experiment 1---------------------------------------
    if set_name.__contains__('Experiment 1/set1'):
        colors = {'Mg': no_variation,
                  'Si': no_variation,
                  'Ti': no_variation
                  }
        patterns = {'Mg': '',
                    'Si': '',
                    'Ti': ''
                    }
    elif set_name.__contains__('Experiment 1/set2'):
        colors = {'Mg': no_variation,
                  'Si': no_variation,
                  'Ti': no_variation,
                  'Fe': no_variation
                  }
        patterns = {'Mg': '',
                    'Si': '',
                    'Ti': '',
                    'Fe': '',
                    }
    elif set_name.__contains__('Experiment 1/set3'):
        colors = {'Mg': variation_one,
                  'Si': no_variation,
                  'Ti': variation_one,
                  'C': no_variation,
                  'O': no_variation,
                  }
        patterns = {'Mg': '',
                    'Si': '',
                    'Ti': '',
                    'C': '',
                    'O': '',
                    }
    elif set_name.__contains__('Experiment 1/set4'):
        colors = {'Mg': no_variation,
                  'Si': no_variation,
                  'Ti': no_variation,
                  'Fe': no_variation,
                  'C': no_variation,
                  'O': no_variation,
                  }
        patterns = {'Mg': '',
                    'Si': '',
                    'Ti': '',
                    'Fe': '',
                    'C': '',
                    'O': '',
                    }
    elif set_name.__contains__('Experiment 1/set5'):
        colors = {'Cr': no_variation,
                  'Mn': no_variation,
                  'Ca': variation_one,
                  'Ti': variation_one,
                  'Y': variation_one,
                  'Si': variation_three,
                  'O': variation_three,
                  'C': variation_two,
                  'Al': variation_two,
                  'Ni': no_variation,
                  'Mg': no_variation,
                  'V': no_variation,
                  'Na': no_variation,
                  }
        patterns = {'Cr': '',
                    'Mn': '',
                    'Ca': '//..',
                    'Ti': '..xx',
                    'Y': 'xx',
                    'Si': '',
                    'O': '//',
                    'C': '',
                    'Al': '',
                    'Ni': '',
                    'Mg': '',
                    'V': '',
                    'Na': '',
                    }
    elif set_name.__contains__('Experiment 1/set6'):
        colors = {'Cr': no_variation,
                  'Mn': no_variation,
                  'Ca': variation_one,
                  'Ti': variation_one,
                  'Y': variation_one,
                  'Si': variation_one,
                  'O': variation_one,
                  'Fe': no_variation,
                  'C': no_variation,
                  'Al': variation_two,
                  'Ni': variation_two,
                  'Mg': variation_two,
                  'V': no_variation,
                  'Na': no_variation,
                  }
        patterns = {'Cr': '',
                    'Mn': '',
                    'Ca': '//oo',
                    'Ti': '//oo',
                    'Y': 'oo',
                    'Si': 'oo',
                    'O': '',
                    'Fe': '',
                    'C': '',
                    'Al': '..',
                    'Ni': '..',
                    'Mg': '',
                    'V': '',
                    'Na': '',
                    }
    elif set_name.__contains__('Experiment 1/set7'):
        colors = {'Si/Mg': variation_one,
                  'Ti/Mg': no_variation,
                  'Fe/Mg': no_variation,
                  'Ca/Mg': variation_one,
                  }
        patterns = {'Si/Mg': '',
                    'Ti/Mg': '',
                    'Fe/Mg': '',
                    'Ca/Mg': '',
                    }
    elif set_name.__contains__('Experiment 1/set8'):
        colors = {'Si/Mg': variation_one,
                  'Ti/Mg': variation_one,
                  'Fe/Mg': no_variation,
                  'Ca/Mg': variation_one,
                  'C/Mg': no_variation,
                  'O/Mg': no_variation,
                  }
        patterns = {'Si/Mg': '',
                    'Ti/Mg': '//',
                    'Fe/Mg': '',
                    'Ca/Mg': '//',
                    'C/Mg': '',
                    'O/Mg': '',
                    }
    elif set_name.__contains__('Experiment 1/set9'):
        colors = {'O/Si': no_variation,
                  'C/Si': no_variation,
                  'Mg/Si': no_variation,
                  'Ti/Si': no_variation,
                  'Fe/Si': no_variation,
                  'Ca/Si': no_variation,
                  }
        patterns = {'O/Si': '',
                    'C/Si': '',
                    'Mg/Si': '',
                    'Ti/Si': '',
                    'Fe/Si': '',
                    'Ca/Si': '',
                    }
    elif set_name.__contains__('Experiment 1/setm10'):
        colors = {'C/O': no_variation,
                  'Si/O': variation_one,
                  'Ti/O': variation_one,
                  'Fe/O': no_variation,
                  'Ca/O': no_variation,
                  'Mg/O': no_variation,
                  }
        patterns = {'C/O': '',
                    'Si/O': '',
                    'Ti/O': '',
                    'Fe/O': '',
                    'Ca/O': '',
                    'Mg/O': '',
                    }
    elif set_name.__contains__('Experiment 1/setm11'):
        colors = {'Fe': no_variation,
                  'Mg': no_variation,
                  'Na': no_variation,
                  'Fe/Mg': no_variation,
                  'Fe/Si': no_variation,
                  'C/Mg': no_variation,
                  'Mg/O': no_variation
                  }
        patterns = {'Fe': '',
                    'Mg': '',
                    'Na': '',
                    'Fe/Mg': '',
                    'Fe/Si': '',
                    'C/Mg': '',
                    'Mg/O': '',
                    }

    ## -----Experiment 2---------------------------------------

    elif set_name.__contains__('Experiment 2/set3'):
        colors = {'Mg': no_variation,
                  'Si': variation_one,
                  'Ti': no_variation,
                  'C': variation_one,
                  'O': no_variation,
                  }
        patterns = {'Mg': '',
                    'Si': '',
                    'Ti': '',
                    'C': '',
                    'O': '',
                    }
    elif set_name.__contains__('Experiment 2/set4'):
        colors = {'Mg': no_variation,
                  'Si': variation_one,
                  'Ti': variation_one,
                  'Fe': no_variation,
                  'C': no_variation,
                  'O': no_variation,
                  }
        patterns = {'Mg': '',
                    'Si': '',
                    'Ti': '',
                    'Fe': '',
                    'C': '',
                    'O': '',
                    }
    elif set_name.__contains__('Experiment 2/set5'):
        colors = {'Cr': variation_three,
                  'Mn': no_variation,
                  'Ca': variation_three,
                  'Ti': variation_two,
                  'Y': variation_two,
                  'Si': variation_three,
                  'O': no_variation,
                  'C': variation_two,
                  'Al': variation_one,
                  'Ni': no_variation,
                  'Mg': variation_one,
                  'V': no_variation,
                  'Na': no_variation,
                  }
        patterns = {'Cr': '',
                    'Mn': '',
                    'Ca': '',
                    'Ti': '',
                    'Y': '',
                    'Si': '',
                    'O': '',
                    'C': '',
                    'Al': '',
                    'Ni': '',
                    'Mg': '',
                    'V': '',
                    'Na': '',
                    }
    elif set_name.__contains__('Experiment 2/set6'):
        colors = {'Cr': variation_five,
                  'Mn': no_variation,
                  'Ca': variation_five,
                  'Ti': variation_four,
                  'Y': variation_three,
                  'Si': variation_five,
                  'O': variation_four,
                  'Fe': variation_three,
                  'C': variation_three,
                  'Al': variation_two,
                  'Ni': variation_one,
                  'Mg': variation_two,
                  'V': variation_one,
                  'Na': no_variation,
                  }
        patterns = {'Cr': '',
                    'Mn': '',
                    'Ca': '',
                    'Ti': '',
                    'Y': '',
                    'Si': '',
                    'O': '',
                    'Fe': '',
                    'C': '',
                    'Al': '',
                    'Ni': '',
                    'Mg': '',
                    'V': '',
                    'Na': '',
                    }
    elif set_name.__contains__('Experiment 2/set7'):
        colors = {'Si/Mg': variation_one,
                  'Ti/Mg': variation_one,
                  'Fe/Mg': no_variation,
                  'Ca/Mg': variation_one,
                  }
        patterns = {'Si/Mg': '',
                    'Ti/Mg': '',
                    'Fe/Mg': '',
                    'Ca/Mg': '',
                    }
    elif set_name.__contains__('Experiment 2/set8'):
        colors = {'Si/Mg': variation_one,
                  'Ti/Mg': no_variation,
                  'Fe/Mg': no_variation,
                  'Ca/Mg': variation_one,
                  'C/Mg': variation_one,
                  'O/Mg': no_variation,
                  }
        patterns = {'Si/Mg': '',
                    'Ti/Mg': '',
                    'Fe/Mg': '',
                    'Ca/Mg': '',
                    'C/Mg': '',
                    'O/Mg': '',
                    }
    elif set_name.__contains__('Experiment 2/set9'):
        colors = {'O/Si': no_variation,
                  'C/Si': no_variation,
                  'Mg/Si': variation_one,
                  'Ti/Si': variation_one,
                  'Fe/Si': no_variation,
                  'Ca/Si': no_variation,
                  }
        patterns = {'O/Si': '',
                    'C/Si': '',
                    'Mg/Si': '',
                    'Ti/Si': '',
                    'Fe/Si': '',
                    'Ca/Si': '',
                    }
    elif set_name.__contains__('Experiment 2/setm10'):
        colors = {'C/O': variation_one,
                  'Si/O': variation_one,
                  'Ti/O': no_variation,
                  'Fe/O': no_variation,
                  'Ca/O': no_variation,
                  'Mg/O': no_variation,
                  }
        patterns = {'C/O': '',
                    'Si/O': '',
                    'Ti/O': '',
                    'Fe/O': '',
                    'Ca/O': '',
                    'Mg/O': '',
                    }
    elif set_name.__contains__('Experiment 2/setm11'):
        colors = {'Fe': no_variation,
                  'Mg': no_variation,
                  'Na': no_variation,
                  'Fe/Mg': no_variation,
                  'Fe/Si': no_variation,
                  'C/Mg': no_variation,
                  'Mg/O': no_variation
                  }
        patterns = {'Fe': '',
                    'Mg': '',
                    'Na': '',
                    'Fe/Mg': '',
                    'Fe/Si': '',
                    'C/Mg': '',
                    'Mg/O': '',
                    }

    ## -----Experiment 3---------------------------------------
    elif set_name.__contains__('Experiment 3/set3'):
        colors = {'Mg': no_variation,
                  'Si': variation_two,
                  'Ti': variation_one,
                  'C': variation_one,
                  'O': variation_two,
                  }
        patterns = {'Mg': '',
                    'Si': '',
                    'Ti': '',
                    'C': '',
                    'O': '',
                    }
    elif set_name.__contains__('Experiment 3/set4'):
        colors = {'Mg': no_variation,
                  'Si': variation_two,
                  'Ti': variation_one,
                  'Fe': variation_one,
                  'C': variation_one,
                  'O': variation_two,
                  }
        patterns = {'Mg': '',
                    'Si': '',
                    'Ti': '',
                    'Fe': '',
                    'C': '',
                    'O': '',
                    }
    elif set_name.__contains__('Experiment 3/set5'):
        colors = {'Cr': no_variation,
                  'Mn': variation_three,
                  'Ca': no_variation,
                  'Ti': variation_two,
                  'Y': variation_one,
                  'Si': variation_three,
                  'O': variation_two,
                  'C': no_variation,
                  'Al': variation_one,
                  'Ni': variation_one,
                  'Mg': variation_one,
                  'V': no_variation,
                  'Na': no_variation,
                  }
        patterns = {'Cr': '',
                    'Mn': '',
                    'Ca': '',
                    'Ti': '',
                    'Y': '',
                    'Si': '',
                    'O': '',
                    'C': '',
                    'Al': '',
                    'Ni': '',
                    'Mg': '',
                    'V': '',
                    'Na': '',
                    }
    elif set_name.__contains__('Experiment 3/set6'):
        colors = {'Cr': no_variation,
                  'Mn': variation_three,
                  'Ca': variation_three,
                  'Ti': variation_three,
                  'Y': variation_two,
                  'Si': variation_three,
                  'O': variation_three,
                  'Fe': variation_three,
                  'C': no_variation,
                  'Al': variation_one,
                  'Ni': variation_three,
                  'Mg': variation_two,
                  'V': variation_one,
                  'Na': no_variation,
                  }
        patterns = {'Cr': '',
                    'Mn': '',
                    'Ca': '',
                    'Ti': '//',
                    'Y': '',
                    'Si': '',
                    'O': '//',
                    'Fe': '',
                    'C': '',
                    'Al': '',
                    'Ni': '//',
                    'Mg': '',
                    'V': '',
                    'Na': '',
                    }
    elif set_name.__contains__('Experiment 3/set8'):
        colors = {'Si/Mg': no_variation,
                  'Ti/Mg': variation_one,
                  'Fe/Mg': no_variation,
                  'Ca/Mg': variation_one,
                  'C/Mg': no_variation,
                  'O/Mg': no_variation,
                  }
        patterns = {'Si/Mg': '',
                    'Ti/Mg': '',
                    'Fe/Mg': '',
                    'Ca/Mg': '',
                    'C/Mg': '',
                    'O/Mg': '',
                    }
    elif set_name.__contains__('Experiment 3/set9'):
        colors = {'O/Si': variation_two,
                  'C/Si': no_variation,
                  'Mg/Si': no_variation,
                  'Ti/Si': variation_two,
                  'Fe/Si': variation_one,
                  'Ca/Si': variation_one,
                  }
        patterns = {'O/Si': '//',
                    'C/Si': '',
                    'Mg/Si': '',
                    'Ti/Si': '',
                    'Fe/Si': '',
                    'Ca/Si': '//',
                    }
    elif set_name.__contains__('Experiment 3/setm10'):
        colors = {'C/O': no_variation,
                  'Si/O': no_variation,
                  'Ti/O': no_variation,
                  'Fe/O': no_variation,
                  'Ca/O': no_variation,
                  'Mg/O': no_variation,
                  }
        patterns = {'C/O': '',
                    'Si/O': '',
                    'Ti/O': '',
                    'Fe/O': '',
                    'Ca/O': '',
                    'Mg/O': '',
                    }
    elif set_name.__contains__('Experiment 3/setm11'):
        colors = {'Fe': variation_one,
                  'Mg': no_variation,
                  'Na': variation_one,
                  'Fe/Mg': no_variation,
                  'Fe/Si': variation_two,
                  'C/Mg': no_variation,
                  'Mg/O': variation_two
                  }
        patterns = {'Fe': '',
                    'Mg': '',
                    'Na': '',
                    'Fe/Mg': '',
                    'Fe/Si': '',
                    'C/Mg': '',
                    'Mg/O': '',
                    }
    
    return colors, patterns


## -----Bar Plot---------------------------------------

#print(feat_imp)
#print(error)

# Merge Feature Importance and Errors
fa = pd.concat([feat_imp,error],axis=1)

# Sort the pandas array by the feature importance
sa = fa.sort_values(by=0)

if(molar):
    for i in range(0,len(sa)):
        sa.index.values[i] = sa.index.values[i].replace('_','/')

# Create the plot
colors = [switch(set_name)[0][i] for i in sa.index.values]
hatches = [switch(set_name)[1][i] for i in sa.index.values]
fig, ax = plt.subplots()
hbars = ax.barh(sa.index.values,
                sa[0], xerr=sa[1],
                edgecolor="black",capsize=4,
                color=colors,
                hatch=hatches,
                )
plt.xlim(0,1.4)
ax.set_xlabel('Weighted Feature Importance Score')
ax.set_ylabel('Feature')
#ax.set_title('Feature Importance')

# Text Legend for plot

## -----Experiment 1---------------------------------------
if (set_name.__contains__('Experiment 1/set1') or
    set_name.__contains__('Experiment 1/set2') or
    set_name.__contains__('Experiment 1/set4') or
    set_name.__contains__('Experiment 1/setm11') or
    set_name.__contains__('Experiment 3/setm10')):
    ax.text(x=1.0,y=-0.4,s='Blue: No Variation')

if (set_name.__contains__('Experiment 1/set3') or
    set_name.__contains__('Experiment 1/set7') or
    set_name.__contains__('Experiment 1/set9') or
    set_name.__contains__('Experiment 1/setm10') or
    set_name.__contains__('Experiment 2/set3') or
    set_name.__contains__('Experiment 2/set4') or
    set_name.__contains__('Experiment 2/set7') or
    set_name.__contains__('Experiment 2/set8') or
    set_name.__contains__('Experiment 2/set9') or
    set_name.__contains__('Experiment 2/setm10') or
    set_name.__contains__('Experiment 2/setm11') or
    set_name.__contains__('Experiment 2/set3') or
    set_name.__contains__('Experiment 2/set4') or
    set_name.__contains__('Experiment 3/set8') or
    set_name.__contains__('Experiment 3/setm11')):
    ax.text(x=0.85,y=-0.1,s='Blue: No Variation')
    ax.text(x=0.85,y=-0.4,s='Colors: Feature Variations')

if (set_name.__contains__('Experiment 1/set5') or
    set_name.__contains__('Experiment 1/set6') or
    set_name.__contains__('Experiment 3/set6')):
    ax.text(x=0.8,y=1.5,s='Blue: No Variation')
    ax.text(x=0.8,y=0.5,s='Colors: Feature Variation')
    ax.text(x=0.8,y=-0.5,s='Patterns: Sub-Group Variation')

if (set_name.__contains__('Experiment 1/set8')):
    ax.text(x=0.8,y=0.2,s='Blue: No Variation')
    ax.text(x=0.8,y=-0.1,s='Colors: Feature Variation')
    ax.text(x=0.8,y=-0.4,s='Patterns: Sub-Group Variation')
    
## -----Experiment 2---------------------------------------

if (set_name.__contains__('Experiment 2/set5') or
    set_name.__contains__('Experiment 2/set6')):
    ax.text(x=0.8,y=0.5,s='Blue: No Variation')
    ax.text(x=0.8,y=-0.1,s='Colors: Feature Variation')

## -----Experiment 3---------------------------------------

if (set_name.__contains__('Experiment 3/set5')):
    ax.text(x=0.8,y=0.5,s='Blue: No Variation')
    ax.text(x=0.8,y=-0.1,s='Colors: Feature Variation')

#Show the plot
plt.show()

## -----End---------------------------------------
