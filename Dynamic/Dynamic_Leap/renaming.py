import os
from os import path
import shutil

Source_Path = '/home/aganguly/Desktop/Dynamic_Leap/Index_flexion'
Destination = '/home/aganguly/Desktop/Dynamic_Leap/Index_flexion_leap'
#dst_folder = os.mkdir(Destination)


def main():
    for count, filename in enumerate(os.listdir(Source_Path)):
        dst =  "Index_flexion_trial" + str(count) + ".csv"

        # rename all the files
        os.rename(os.path.join(Source_Path, filename),  os.path.join(Destination, dst))


# Driver Code
if __name__ == '__main__':
    main()