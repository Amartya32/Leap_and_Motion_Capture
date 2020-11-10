# Leap_and_Motion_Capture

Paper Title: <b>Performance of the Leap Motion Controller synchronised with standard markered motion capture</b><br>
Journal    : <b>Sensors (https://www.mdpi.com/journal/sensors)</b><br>
Authors    : <b>Amartya Ganguly<sup>1*</sup>, Gabriel Rashidi<sup>1</sup>, and Katja Mombaur<sup>2</sup> </b><br>

1. Optimization, Robotics and Biomechanics, Institute of Computer Engineering, Heidelberg University, 69120,Heidelberg, Germany<br>
2. Canada Excellence Chair in Human-Centred Robotics and Machine Intelligence, University of Waterloo,Waterloo, ON N2L 3G1, Canada.;
katja.mombaur@uwaterloo.ca<br>
*Correspondence: amartya.ganguly@ziti.uni-heidelberg.de<br>

# Leap Motion Controller
All relevant information regarding Leap development SDK can be found here.<br>
https://developer-archive.leapmotion.com/documentation/python/index.html

A quick introduction on how to conncect the Leap Motion Controller and output the data can be found here:<br>
https://developer-archive.leapmotion.com/documentation/python/devguide/Sample_Tutorial.html <br>
Parts of the code snippets like the *SampleListener* Class, the *main* function as well as the *on_frame* function are also used in this code.<br><br>
The following gives you brief overview of the synchronisation code provided in this repo:<br>
<ul>
  
  <li>main code block</li>
  <ul>
    <li> this part updates the file counter for the runs and prints the header of the text files<br>
    <li> produces two folders: processed and postProcessed<br>
    <li> processed folder contains the data which has the 1 set in the status_qtm column<br>
    <li> postProcessed folder contains data sorted by finger names</li>
  </ul>
  
  <li> <em>main</em> function</li>
  <ul>
    <li> creates listener and contoller instances; controls the program exit; press enter to stop and exit from the while loop<br> 
    <li> sets the policy of the Leap Controller to background so the data acquisition can continue while other programs run</li>
  </ul>
  
  <li> <em>SampleListener</em> class</li>
  <ul>
    <li> <em>on_connect</em>: prints conncected when your leap device connects succesfully</li>
    <li> <em>on_frame</em>: fetches the data of each frame and writes them into separate textfiles for both hands each<br>
      Textfiles for each run will be put into the rawData folder and named lefthand <b>N</b> and righthand <b>N</b>, where, <b>N</b> is the counter refering to the runs starting at 1</li>
      </ul>
      
  <li> <em>Server</em> class</li>
  <ul>
    <li> implements a background server on a second thread which runs parallel to the main program and listens on a UDP socket to incoming events from QTM on port 8888, which is the default port of QTM sending out data</li>
    <li> default interface the is the loopback interface which refers to the machine this servers on</li>
    <if no parameters are given the program will use default confgurations</li>
    <li> the server is responsible for updating the golbal <em>status_qtm</em> variable which gets written into the output textfile and indicates the intervals in which QTM was capturing data while running the Leap Motion Controller</li>
    <li> this intervalls are consecutive leap data frames which have a 1 in their status_qtm column</li>
  </ul>
  
  <li> <em>sortFingersByName</em></li>
  <ul>
    <li> sorts the fingers by name in this order: Thumb, Index, Middle, Ring, Pinky.<br>This is required for plotting procedures.</li>
  </ul>
  
  <li> <em>sanitiseArray</em></li>
  <ul>
    <li> removes opening and closing brackets from (x, y, z) tuples </li>
  </ul>
  
</ul>
  

Running the script and QTM on the same machine
------------------------------------------
Script depends on Python2 code. Run it by starting the Windows Powershell and the command: python2 leapDataExtraction.py

The script takes an optional parameter, the IP address of the network interface of the machine which runs the QTM programme. By default, it is set to the loop-back interface. 

Running the script and QTM on different machines
--------------------------------------------
However, to run this script on a different machine from which QTM is running, then the script needs the IP address of the machine which runs QTM. Eduroam does not allow unathorized UDP-SocketStreams. Log in the machine into a different WiFi, e.g. Heidelberg4You. Obtain the IP address when using the Windows Commandline (cmd) on the machine running QTM and run the command: ipconfig. 

Obtain IPv4-address from the WiFi interface and give it as a string argument to the script (python2 leapDataExtraction.py "IPv4 address from WiFi interface"). The server of the script will listen to this interface and run the script and QTM on the same machine. 

Warning: The machines logged in into the public WiFis will log out after some time automatically so before you start your measurement check if you are still connected to the public WiFi. (in case of public WIFI).


Examples of dynamic movements of one subject
--------------------------------------------

Thumb flexion
![me](thumb_flexion.gif)


Funding
-------

This project was funded by <b>EIT Health under grant id: 19340</b>



Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg
