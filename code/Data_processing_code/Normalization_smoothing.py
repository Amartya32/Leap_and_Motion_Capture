# ### This code is formulated for Batch processing of files ###################

# The processing steps are as follows
# 1. Load all raw data files
# 2. Data is normalised and smoothened.


import glob
import pandas as pd
from tnorma import tnorma # https://pypi.org/project/tnorma/ # Duarte, M. (2020) tnorma: A Python module for temporal normalization (from 0 to 100% with step interval), https://github.com/demotu/tnorma.
import seaborn as sns
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Enter the path of the folder which contains the interpolated and filtered data of either Leap or Motion capture files
path = r"/home/aganguly/Desktop/aganguly/Dynamic_Leap/Index_flex_ext/Original_Index_Leap/Interpolated_Filtered_Leap_Index_Flex"

all_files = glob.glob(path + "/*.csv")


yn = []

for filename in all_files:
    d = pd.read_csv(filename)
    
    print(filename)
    foo = filename.split("/")[-1]
   

    output = d.to_numpy(dtype = 'f')
    
    yn, tn, indie = tnorma(output, k=3, smooth=1, mask=None, show=False) # Time normalisation and smoothing 
    print("/home/aganguly/Desktop/aganguly/Dynamic_Leap/Index_flex_ext/Original_Index_Leap/Interpolated_Filtered_Leap_Index_Flex" + filename)
    # Create a  new folder to save the time normalised data (All calculations are done after the processing is complete)
    np.savetxt(
        "/home/aganguly/Desktop/aganguly/Dynamic_Leap/Index_flex_ext/Original_Index_Leap/Interpolated_Filtered_Leap_Index_Flex/Normalised_Displacement_Index_Flex/"
        + foo,
        yn,
        delimiter=", ",
        newline="\n",
    )


