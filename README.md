# Leap_and_Motion_Capture

Paper Title: <b>Performance of the Leap Motion Controller synchronised with standard markered motion capture</b><br>
Journal    : <b>Sensors (https://www.mdpi.com/journal/sensors)</b><br>
Authors    : <b>Amartya Ganguly<sup>1*</sup>, Gabriel Rashidi<sup>1</sup>, and Katja Mombaur<sup>2</sup> </b><br>

1. Optimization, Robotics and Biomechanics, Institute of Computer Engineering, Heidelberg University, 69120,Heidelberg, Germany<br>
2. Canada Excellence Chair in Human-Centred Robotics and Machine Intelligence, University of Waterloo,Waterloo, ON N2L 3G1, Canada.;
katja.mombaur@uwaterloo.ca<br>
*Correspondence: amartya.ganguly@ziti.uni-heidelberg.de<br>

# Leap Motion Controller
All relevant information regarding leap development can be found here.<br>
https://developer-archive.leapmotion.com/documentation/python/index.html

A quick introduction on how to conncect the leap controller and output the data can be found here:<br>
https://developer-archive.leapmotion.com/documentation/python/devguide/Sample_Tutorial.html <br>
Parts of the code snippets like the SampleListener Class, the main function as well as the on_frame function are also used in this code.<br><br>
The following gives you brief overview on the code provided in this repo:<br>
<ul>
  <li>main code block</li>
  <ul>
    <li>this part updates the file counter for the runs and prints the header of the text files<br>
      it also produces two folders: processed and postProcessed<br>
      the processed folder contains the data which has the 1 set in the status_qtm column<br>
      the postProcessed folder contains the the same data as the processed folder but sorted by finger names</li>
  </ul>
  <li>main function</li>
  <ul>
    <li>the main, creates listener and contoller instances and controls the program exit so if you press enter the program will stop and exit the while loop<br>it also sets the policy of the leap controller to background so the data acquisition can happen in the background while you run other programs</li>
  </ul>
  <li>SampleListener class</li>
  <ul>
    <li>on_connect: prints conncected when your leap device connects succesfully</li>
    <li>on_frame: fetches the data of each frame and writes them into separate textfiles for both hands each<br>
      the textfiles for each run will be put into the rawData folder and named lefthand <b>N</b> and righthand <b>N</b> where <b>N</b> is the counter refering to the runs starting at 1</li>
      </ul>
  <li>Server class</li>
  <ul>
    <li>implements a background server on a second thread which runs parallel to the main program and listens on a udp socket to incoming events from qtm on port 8888, which is the default port of qtm sending out data</li>
    <li>default interface the is the loopback interface which refers to the machine this servers on</li>
    <if you dont give the program any parameters then it will use this default confgurations</li>
    <li>the server is responsible for updating the golbal status_qtm variable which gets written into the outout textfile and indicates the intervalls in which qtm was capturing data while running the leap</li>
    <li>this intervalls are consecutive leap data frames which have a 1 in their status_qtm column</li>
  </ul>
  <li>sortFingersByName</li>
  <ul>
    <li> sorts the fingers by name in this order: Thumb, Index, Middle, Ring, Pinky.<br>This may be required for some                                        plotting procedures.</li>
  </ul>
  <li>sanitiseArray</li>
  <ul>
    <li>removes opening and closing brackets from (x, y, z) tuples as you dont want those in your data</li>
  </ul>
</ul>
  



Starting procedure
------------------
Script depends on Python2 code so you should run it with Python2. If you use the machine in the lab Python 2 is already preinstalled. You can run it by starting the Windows Powershell
and run the command: python2 leapDataExtraction.py for running this script.

Running the script and QTM on the same machine
------------------------------------------
The script takes an optional parameter which is the IP address of the network interface of the machine which is running the QTM programm. By default it is set to the loopback interface,
so if QTM is running on the same machine where you are running this script then everything is fine and you do not need to provide any arguments in the commandline to script.

Running the script and QTM on different machines
--------------------------------------------
However if you wish to run this script on a different machine from which QTM is running on then you will need to give the script the IP address of the machine which is running QTM.
As eduroam does not allow unathorized UDP-SocketStreams you will have first to log in the machine into a different WIFI e.g. Heidelberg4You.
You can get the IP address if you start the  Windows Commandline (cmd) on the machine running QTM and run the command: ipconfig. Get IPv4-address from the WIFI Interface and give it as a
string argument to the script (python2 leapDataExtraction.py "IPv4 address from WIFI interface"). The server of the script will now listen to this interface and you can proceed as if you would run
the script and QTM on the same machine. Be careful the machines logged in into the public WIFIs will log out after some time automatically so before you start your measurement check if you
are still connected to the public WIFI (in case you use a public WIFI).



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
