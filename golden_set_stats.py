import numpy as np
import os
import pandas as pd
import matplotlib as plt
import sys
from glob import glob

# Define file locations
experiment = 'All'
work_dir = os.path.dirname(os.path.realpath(__file__))
path = os.path.dirname(os.path.realpath(__file__)) + '\\Golden Set Files\\' + experiment + '\\'

df = pd.DataFrame(columns=["star_name","Sampled","Predicted","Prob"])

for file in glob(path+"goldenSetProbabilities*.csv"):
    golden_file = pd.read_csv(file, usecols=["star_name","Sampled","Predicted","Prob"])
    df = pd.concat([df,golden_file])

df.to_csv("golden_set_all.csv")
