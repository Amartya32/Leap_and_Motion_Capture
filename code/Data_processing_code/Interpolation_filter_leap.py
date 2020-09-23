# This code is processes the raw data files taken from Leap 
# The processing steps are as follows
# 1. Load all raw data files
# 2. Sort the desired Finger (Thumb, Index, Middle, Ring, Pinky)
# 3. Creat a new time vector because Leap data streaming is not in a constant frequency
# 4. Perform Interpolation
# 5. Perform Low Pass filtering
# 6. Save the data in seperate files for further processing.
### This code is formulated for Batch processing of files #####################

import glob
import pandas as pd
import seaborn as sns
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

# Enter the path of the folder which contains all the raw original files of Leap Motion Capture Data
path = r"/home/aganguly/Desktop/aganguly/Dynamic_Leap/Index_flex_ext/Original_Index_Leap"

all_files = glob.glob(path + "/*.csv")

output = []

for filename in all_files:
    d = pd.read_csv(filename)
    
    
    foo = filename.split("/")[-1]
    Thumb   = d[d['name'].str.match('Thumb')]
    Index   = d[d['name'].str.match('Index')]
    Middle  = d[d['name'].str.match('Middle')]
    Ring    = d[d['name'].str.match('Ring')]
    Pinky    = d[d['name'].str.match('Pinky')]
    
    T = Index.iloc[:,13:] # T = [Insert Name of the Finger as Appropriate e.g Index, Middle..etc. as shown].iloc[:,13:] 

    WX = T.to_numpy()
    

    Fps1   = T.iloc[:,2]
    Fps   = Fps1.to_numpy()

    
    T = np.zeros(Fps1.shape)
    
    T[0] = 0
    # New time vector
    for i in range (1,len(T[1:])+1):
        T[i] = (T[i-1])+(1/Fps[i])

    ## Interpolation 
    lowPassCutoffFreq = 10.0  # Cut off frequency
    Sample_freq = 150

    timeInterp = np.arange(0, np.max(T), 1/Sample_freq)

    yn = np.zeros(timeInterp.shape)

    yn= interp1d(T,WX[:,0:], axis=0)
    ynew = yn(timeInterp)
        
    # Filtering of data    
    # Target sample frequency
    N = 2  # Order of the filter; In this case 2nd order
    Wn = lowPassCutoffFreq / (Sample_freq / 2)  # Normalize frequency

    b, a = signal.butter(N, Wn, btype="low", analog=False, output="ba")
    # scipy.signal.butter(N, Wn, btype='low', analog=False, output='ba', fs=None)

    output = signal.filtfilt(b, a, ynew, axis=0)

    plt.plot(timeInterp, output, 'blue') 
        plt.show()
    
    # Saving data in multiple files 
    # Create a new folder to save the filtered and interpolated data as the case maybe
    np.savetxt(
        "/home/aganguly/Desktop/aganguly/Dynamic_Leap/Index_flex_ext/Original_Index_Leap/Interpolated_Filtered_Leap_Index_Flex/"
        + foo,
        output,
        delimiter=", ",
        newline="\n",
    )


