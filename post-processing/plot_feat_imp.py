import numpy as np
import pandas as pd
import yaml
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from xgboost import XGBRegressor

## ------Import the Data-----------------------------------------
molar = True
set_name = "experiment-3/set7"
stream = open('{0}/params.yaml'.format(set_name), 'r')
parameters = yaml.load(stream, Loader=yaml.FullLoader)
features = parameters['features']

df = pd.read_csv('main.csv')
results = pd.read_pickle('{0}/df_info_all.pkl'.format(set_name))

data = pd.read_pickle('{0}/features_train.pkl'.format(set_name))

if data.columns[0].__contains__('/'):
    data.columns = [col.replace('/','_') for col in data.columns]

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
    
    if set_name.__contains__(f'experiment-1/set1-golden'):
        colors = {'Mg': no_variation,
                  'Si': no_variation,
                  'Ti': no_variation,
                  'C': no_variation,
                  'O': no_variation,
                  }
        patterns = {'Mg': '',
                    'Si': '',
                    'Ti': '',
                    'C': '',
                    'O': '',
                    }
    elif set_name.__contains__(f'experiment-1/set2-golden'):
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
    elif set_name.__contains__(f'experiment-1/set3-golden'):
        colors = {'Cr': no_variation,
                  'Mn': no_variation,
                  'Ca': variation_one,
                  'Ti': variation_one,
                  'Y': variation_one,
                  'Si': no_variation,
                  'O': no_variation,
                  'C': no_variation,
                  'Al': variation_two,
                  'Ni': no_variation,
                  'Mg': variation_two,
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
    elif set_name.__contains__('experiment-1/set4-golden'):
        colors = {'Cr': variation_three,
                  'Mn': variation_three,
                  'Ca': variation_three,
                  'Ti': variation_two,
                  'Y': variation_two,
                  'Si': variation_three,
                  'O': no_variation,
                  'Fe': no_variation,
                  'C': no_variation,
                  'Al': variation_one,
                  'Ni': variation_one,
                  'Mg': variation_one,
                  'V': no_variation,
                  'Na': no_variation,
                  }
        patterns = {'Cr': '',
                    'Mn': '',
                    'Ca': '..',
                    'Ti': '..',
                    'Y': '',
                    'Si': '',
                    'O': '',
                    'Fe': '',
                    'C': '//',
                    'Al': '//',
                    'Ni': '',
                    'Mg': '',
                    'V': '',
                    'Na': '',
                    }
    elif set_name.__contains__('experiment-1/set5-golden'):
        colors = {'Si/Mg': no_variation,
                  'Ti/Mg': no_variation,
                  'Fe/Mg': no_variation,
                  'Ca/Mg': no_variation,
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
    elif set_name.__contains__('experiment-1/set6-golden'):
        colors = {'O/Si': no_variation,
                  'C/Si': no_variation,
                  'Mg/Si': variation_one,
                  'Ti/Si': variation_one,
                  'Fe/Si': variation_one,
                  'Ca/Si': no_variation,
                  }
        patterns = {'O/Si': '',
                    'C/Si': '',
                    'Mg/Si': '',
                    'Ti/Si': '',
                    'Fe/Si': '',
                    'Ca/Si': '',
                    }
    elif set_name.__contains__('experiment-1/set7-golden'):
        colors = {'C/O': variation_one,
                  'Si/O': no_variation,
                  'Ti/O': no_variation,
                  'Fe/O': variation_one,
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

    ## -----Experiment 2---------------------------------------

    elif set_name.__contains__('experiment-2/set1'):
        colors = {'Mg': no_variation,
                  'Si': no_variation,
                  'Ti': no_variation,
                  'C': no_variation,
                  'O': no_variation,
                  }
        patterns = {'Mg': '',
                    'Si': '',
                    'Ti': '',
                    'C': '',
                    'O': '',
                    }
    elif set_name.__contains__('experiment-2/set2'):
        colors = {'Mg': variation_one,
                  'Si': variation_two,
                  'Ti': no_variation,
                  'Fe': variation_one,
                  'C': no_variation,
                  'O': variation_two,
                  }
        patterns = {'Mg': '',
                    'Si': '',
                    'Ti': '',
                    'Fe': '',
                    'C': '',
                    'O': '',
                    }
    elif set_name.__contains__('experiment-2/set3'):
        colors = {'Cr': variation_two,
                  'Mn': no_variation,
                  'Ca': variation_two,
                  'Ti': variation_one,
                  'Y': variation_one,
                  'Si': variation_two,
                  'O': variation_one,
                  'C': variation_one,
                  'Al': variation_three,
                  'Ni': no_variation,
                  'Mg': variation_one,
                  'V': variation_three,
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
    elif set_name.__contains__('experiment-2/set4'):
        colors = {'Cr': variation_three,
                  'Mn': variation_three,
                  'Ca': no_variation,
                  'Ti': variation_one,
                  'Y': variation_one,
                  'Si': no_variation,
                  'O': variation_one,
                  'Fe': variation_one,
                  'C': variation_one,
                  'Al': no_variation,
                  'Ni': variation_two,
                  'Mg': variation_one,
                  'V': variation_two,
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
    elif set_name.__contains__('experiment-2/set5'):
        colors = {'Si/Mg': variation_one,
                  'Ti/Mg': variation_two,
                  'Fe/Mg': no_variation,
                  'Ca/Mg': variation_two,
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
    elif set_name.__contains__('experiment-2/set6'):
        colors = {'O/Si': no_variation,
                  'C/Si': no_variation,
                  'Mg/Si': variation_one,
                  'Ti/Si': variation_one,
                  'Fe/Si': variation_one,
                  'Ca/Si': variation_one,
                  }
        patterns = {'O/Si': '',
                    'C/Si': '',
                    'Mg/Si': '',
                    'Ti/Si': '',
                    'Fe/Si': '',
                    'Ca/Si': '',
                    }
    elif set_name.__contains__('experiment-2/set7'):
        colors = {'C/O': variation_one,
                  'Si/O': no_variation,
                  'Ti/O': variation_two,
                  'Fe/O': variation_one,
                  'Ca/O': variation_two,
                  'Mg/O': no_variation,
                  }
        patterns = {'C/O': '',
                    'Si/O': '',
                    'Ti/O': '',
                    'Fe/O': '',
                    'Ca/O': '',
                    'Mg/O': '',
                    }

    ## -----Experiment 3---------------------------------------
    elif set_name.__contains__('experiment-3/set1'):
        colors = {'Mg': no_variation,
                  'Si': no_variation,
                  'Ti': variation_one,
                  'C': variation_one,
                  'O': no_variation,
                  }
        patterns = {'Mg': '',
                    'Si': '',
                    'Ti': '',
                    'C': '',
                    'O': '',
                    }
    elif set_name.__contains__('experiment-3/set2'):
        colors = {'Mg': no_variation,
                  'Si': no_variation,
                  'Ti': variation_one,
                  'Fe': variation_one,
                  'C': variation_one,
                  'O': variation_one,
                  }
        patterns = {'Mg': '',
                    'Si': '',
                    'Ti': '',
                    'Fe': '',
                    'C': '',
                    'O': '',
                    }
    elif set_name.__contains__('experiment-3/set3'):
        colors = {'Cr': no_variation,
                  'Mn': variation_one,
                  'Ca': variation_one,
                  'Ti': variation_one,
                  'Y': variation_one,
                  'Si': variation_one,
                  'O': variation_one,
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
                    'Ti': '//',
                    'Y': '',
                    'Si': '',
                    'O': '',
                    'C': '',
                    'Al': '',
                    'Ni': '',
                    'Mg': '',
                    'V': '//',
                    'Na': '',
                    }
    elif set_name.__contains__('experiment-3/set4'):
        colors = {'Cr': no_variation,
                  'Mn': variation_one,
                  'Ca': variation_one,
                  'Ti': variation_one,
                  'Y': variation_one,
                  'Si': variation_one,
                  'O': variation_one,
                  'Fe': variation_one,
                  'C': variation_two,
                  'Al': variation_two,
                  'Ni': variation_one,
                  'Mg': variation_one,
                  'V': variation_two,
                  'Na': no_variation,
                  }
        patterns = {'Cr': '',
                    'Mn': '',
                    'Ca': '',
                    'Ti': '//',
                    'Y': '',
                    'Si': '',
                    'O': '',
                    'Fe': '',
                    'C': '',
                    'Al': '//',
                    'Ni': '',
                    'Mg': '',
                    'V': '',
                    'Na': '',
                    }
    elif set_name.__contains__('experiment-3/set5'):
        colors = {'Si/Mg': variation_one,
                  'Ti/Mg': variation_one,
                  'Fe/Mg': variation_one,
                  'Ca/Mg': no_variation,
                  'C/Mg': variation_one,
                  'O/Mg': variation_one,
                  }
        patterns = {'Si/Mg': '',
                    'Ti/Mg': '',
                    'Fe/Mg': '',
                    'Ca/Mg': '',
                    'C/Mg': '',
                    'O/Mg': '',
                    }
    elif set_name.__contains__('experiment-3/set6'):
        colors = {'O/Si': variation_two,
                  'C/Si': variation_one,
                  'Mg/Si': no_variation,
                  'Ti/Si': variation_one,
                  'Fe/Si': variation_two,
                  'Ca/Si': no_variation,
                  }
        patterns = {'O/Si': '',
                    'C/Si': '',
                    'Mg/Si': '',
                    'Ti/Si': '',
                    'Fe/Si': '',
                    'Ca/Si': '',
                    }
    elif set_name.__contains__('experiment-3/set7'):
        colors = {'C/O': no_variation,
                  'Si/O': no_variation,
                  'Ti/O': variation_one,
                  'Fe/O': no_variation,
                  'Ca/O': variation_one,
                  'Mg/O': no_variation,
                  }
        patterns = {'C/O': '',
                    'Si/O': '',
                    'Ti/O': '',
                    'Fe/O': '',
                    'Ca/O': '',
                    'Mg/O': '',
                    }
    
    return colors, patterns


## -----Bar Plot---------------------------------------

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
if (set_name.__contains__(f'experiment-1/set1-golden') or
    set_name.__contains__(f'experiment-1/set2-golden') or
    set_name.__contains__(f'experiment-1/set5-golden') or
    set_name.__contains__('Experiment 1/setm11') or
    set_name.__contains__(f'experiment-2/set1') or
    set_name.__contains__('Experiment 3/setm10')):
    ax.text(x=1.0,y=-0.4,s='Blue: No Variation')

if (set_name.__contains__(f'experiment-1/set3-golden') or
    set_name.__contains__(f'experiment-1/set6-golden') or
    set_name.__contains__(f'experiment-1/set7-golden') or
    set_name.__contains__('Experiment 1/setm10') or
    set_name.__contains__(f'experiment-2/set2') or
    set_name.__contains__(f'experiment-2/set3') or
    set_name.__contains__(f'experiment-2/set4') or
    set_name.__contains__(f'experiment-2/set5') or
    set_name.__contains__(f'experiment-2/set6') or
    set_name.__contains__(f'experiment-2/set7') or
    set_name.__contains__(f'experiment-3/set1') or
    set_name.__contains__(f'experiment-3/set2') or
    set_name.__contains__(f'experiment-3/set5') or
    set_name.__contains__(f'experiment-3/set6') or
    set_name.__contains__(f'experiment-3/set7') or
    set_name.__contains__('Experiment 3/setm11')):
    ax.text(x=0.85,y=0.2,s='Blue: No Variation')
    ax.text(x=0.85,y=-0.4,s='Colors: Feature Variations')

if (set_name.__contains__('Experiment 1/set5') or
    set_name.__contains__('Experiment 1/set6') or
    set_name.__contains__('Experiment 3/set6') or
    set_name.__contains__(f'experiment-3/set3') or
    set_name.__contains__(f'experiment-3/set4')):
    ax.text(x=0.8,y=1.5,s='Blue: No Variation')
    ax.text(x=0.8,y=0.5,s='Colors: Feature Variation')
    ax.text(x=0.8,y=-0.5,s='Patterns: Sub-Group Variation')

if (set_name.__contains__('experiment-1/set4-golden')):
    ax.text(x=0.8,y=0.2,s='Blue: No Variation')
    ax.text(x=0.8,y=-0.4,s='Colors: Feature Variation')
    ax.text(x=0.8,y=-0.95,s='Patterns: Sub-Group Variation')
    
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
