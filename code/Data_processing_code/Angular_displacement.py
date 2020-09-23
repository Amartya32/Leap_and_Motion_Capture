# This code does a Batch calculation of all files
# The code calculates angules from Leap and Mocap data from positional data measured 

import glob
import pandas as pd
import seaborn as sns
import numpy as np


path = r"Enter path where you have stored your normalised folder of specific motion like Index flexion, middle flexion etc."

all_files = glob.glob(path + "/*.csv")


Angles = []

for filename in all_files:
    d = pd.read_csv(filename)
    
    
    foo = filename.split("/")[-1]
    
    d = d.to_numpy(dtype='f')

    W = d[:, 0:3] # Location of wrist values # For Mocap it is different please refer to the paper and .csv files for the correct header and column position
    
    M = d[:, 15:18] # Metacarpal joint position
    P = d[:, 18:21] # Proximal joint position
    D = d[:, 27:30] # Distal joint position
    T = d[:, 36:39] # Finger tip position

    WM = W-M
    MP = M-P
    PD = P-D
    DT = D-T

    def MCP(WM, MP):
        p1 = np.einsum('ij,ij->i',WM,MP)
        p2 = np.einsum('ij,ij->i',WM,WM)
        p3 = np.einsum('ij,ij->i',MP,MP)
        p4 = p1 / np.sqrt(p2*p3)
        return np.arccos(np.clip(p4,-1.0,1.0))

    MCP = MCP(WM, MP)*180/np.pi
    

    def PIP(MP, PD):
        p1 = np.einsum('ij,ij->i',MP,PD)
        p2 = np.einsum('ij,ij->i',MP,MP)
        p3 = np.einsum('ij,ij->i',PD,PD)
        p4 = p1 / np.sqrt(p2*p3)
        return np.arccos(np.clip(p4,-1.0,1.0))

    PIP = PIP(MP, PD)*180/np.pi

    def DIP(PD, DT):
        p1 = np.einsum('ij,ij->i',PD,DT)
        p2 = np.einsum('ij,ij->i',PD,PD)
        p3 = np.einsum('ij,ij->i',DT,DT)
        p4 = p1 / np.sqrt(p2*p3)
        return np.arccos(np.clip(p4,-1.0,1.0))

    DIP = DIP(PD, DT)*180/np.pi 
    

    Angles = np.vstack((MCP, PIP, DIP))
    
    
    print("/home/aganguly/Desktop/aganguly/Dynamic_Leap/Index_flex_ext/Original_Index_Leap/Interpolated_Filtered_Leap_Index_Flex/Normalised_Displacement_Index_Flex" + filename)
    # Save the calucation of angles of each finger with 3 joints in a seperate folder
    np.savetxt(
        "/home/aganguly/Desktop/aganguly/Dynamic_Leap/Index_flex_ext/Original_Index_Leap/Interpolated_Filtered_Leap_Index_Flex/Normalised_Displacement_Index_Flex/Normalised_Angles_Index/"
        + foo,
        Angles.T,
        delimiter=", ",
        newline="\n",
    )

