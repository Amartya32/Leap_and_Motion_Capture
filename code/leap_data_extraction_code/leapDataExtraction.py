
################################################################################
# Copyright (C) 2012-2013 Leap Motion, Inc. All rights reserved.               #
# Leap Motion proprietary and confidential. Not for distribution.              #
# Use subject to the terms of the Leap Motion SDK Agreement available at       #
# https://developer.leapmotion.com/sdk_agreement, or another agreement         #
# between Leap Motion and you, your company or other organization.             #
################################################################################

import os, sys, thread, time, inspect, socket, threading
sys.path.insert(1, '..\windows64')
#sys.path.append('..\leapWinPack')
import Leap
from argparse import ArgumentParser
import numpy as np
from sortFingersByName import *


def sanitiseArray(string):
    cleanString = str()
    string = str(string)
    for e in string:
        if e != '(' and e != ')':
            cleanString += e
    return cleanString


class SampleListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

    def on_connect(self, controller):
        print ("Connected")


    def on_frame(self, controller):
        frame = controller.frame()

        print ("status_qtm: %s, FramePerSec: %d, Frame id: %d, timestamp: %d, hands: %d, fingers: %d" % (
        status_qtm, frame.current_frames_per_second, frame.id, frame.timestamp, len(frame.hands), len(frame.fingers)))

        for hand in frame.hands:
            if hand.is_left:
                print("left")
                for finger in hand.fingers:
                    fl.write("%s,%d,%d," % (status_qtm, frame.current_frames_per_second, frame.id))
                    fl.write("%d,%d,%d," % (frame.timestamp, len(frame.hands), len(frame.fingers)))
                    fl.write("%d,%f," % (finger.id, finger.length))
                    fl.write("%f,%s," % (finger.width, sanitiseArray(hand.arm.direction)))
                    fl.write("%s,%s," % (sanitiseArray(hand.arm.wrist_position), sanitiseArray(hand.arm.elbow_position)))
                    fl.write("%s," % (self.finger_names[finger.type]))
                    for b in range(0, 4):
                        bone = finger.bone(b)
                        fl.write("%s,%s," % (sanitiseArray(bone.prev_joint), sanitiseArray(bone.next_joint)))
                        fl.write("%s," % (sanitiseArray(bone.direction)))
                    fl.write("\n")
            else:
                print("right")
                for finger in hand.fingers:
                    fr.write("%s,%d,%d," % (status_qtm, frame.current_frames_per_second, frame.id))
                    fr.write("%d,%d,%d," % (frame.timestamp, len(frame.hands), len(frame.fingers)))
                    fr.write("%d,%f," % (finger.id, finger.length))
                    fr.write("%f,%s," % (finger.width, sanitiseArray(hand.arm.direction)))
                    fr.write("%s,%s," % (sanitiseArray(hand.arm.wrist_position), sanitiseArray(hand.arm.elbow_position)))
                    fr.write("%s," % (self.finger_names[finger.type]))
                    for b in range(0, 4):
                        bone = finger.bone(b)
                        fr.write("%s,%s," % (sanitiseArray(bone.prev_joint), sanitiseArray(bone.next_joint)))
                        fr.write("%s," % (sanitiseArray(bone.direction)))
                    fr.write("\n")

        print("\n")

#background server listening to events from qtm
class Server(object):
    def __init__(self, interface, port):
        self.interface = interface
        self.port = port
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        global status_qtm
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((self.interface, self.port))

        while True:
            data, addr = sock.recvfrom(1024)
            print(data)
            status_qtm = data

def main():
    #Create a sample listener and controller
    listener = SampleListener()
    controller = Leap.Controller()

    #Have the sample listener receive events from the controller
    controller.add_listener(listener)

    #keep process running in the background
    if not controller.is_policy_set(Leap.Controller.POLICY_BACKGROUND_FRAMES):
        controller.set_policy(Leap.Controller.POLICY_BACKGROUND_FRAMES)

    #Keep this process running until Enter is pressed
    print ("Press Enter to quit...")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        #Remove the sample listener when done
        controller.remove_listener(listener)


if __name__ == "__main__":
    #globale variabel status_qtm: 0 = capture stopped 1 = capture started
    status_qtm = 0

    #get ip adress, default loopback interface
    parser = ArgumentParser(description="leap motion data reader depending on qtm capturing")
    parser.add_argument("--host_qtm", default="127.0.0.1", help="IP address of the network interface of the machine which is running qtm")
    args = parser.parse_args()
    #---

    #open file for left and right hand
    if not os.path.isdir("rawData"):
        os.mkdir("rawData")

    countLeft = 1
    while os.path.exists("rawData/lefthand%s.txt" % countLeft):
        countLeft += 1

    fl = open("rawData/lefthand%s.txt" % countLeft, "w")
    fl.write("begin/end,FramePerSec,Frameid,timestamp,hands,fingers,")
    fl.write("ID,length,width,")
    fl.write("ArmDirX,ArmDirY,ArmDirZ,")
    fl.write("WX,WY,WZ,")
    fl.write("ElbPosX,ElbPosY,ElbPosZ,")
    fl.write("name,")
    fl.write("Metacarpal_BBX,Metacarpal_BBY,Metacarpal_BBZ,")
    fl.write("Metacarpal_BHX,Metacarpal_BHY,Metacarpal_BHZ,")
    fl.write("Metacarpal_BDirX,Metacarpal_BDirY,Metacarpal_BDirZ,")
    fl.write("Proximal_BBX,Proximal_BBY,Proximal_BBZ,")
    fl.write("Proximal_BHX,Proximal_BHY,Proximal_BHZ,")
    fl.write("Proximal_BDirX,Proximal_BDirY,Proximal_BDirZ,")
    fl.write("Intermediate_BBX,Intermediate_BBY,Intermediate_BBZ,")
    fl.write("Intermediate_BHX,Intermediate_BHY,Intermediate_BHZ,")
    fl.write("Intermediate_BDirX,Intermediate_BDirY,Intermediate_BDirZ,")
    fl.write("Distal_BBX,Distal_BBY,Distal_BBZ,")
    fl.write("Distal_BHX,Distal_BHY,Distal_BHZ,")
    fl.write("Distal_BDirX,Distal_BDirY,Distal_BDirZ\n")

    countRight = 1
    while os.path.exists("rawData/righthand%s.txt" % countRight):
        countRight += 1

    fr = open("rawData/righthand%s.txt" % countRight, "w")
    fr.write("begin/end,FramePerSec,Frameid,timestamp,hands,fingers,")
    fr.write("ID,length,width,")
    fr.write("ArmDirX,ArmDirY,ArmDirZ,")
    fr.write("WX,WY,WZ,")
    fr.write("ElbPosX,ElbPosY,ElbPosZ,")
    fr.write("name,")
    fr.write("Metacarpal_BBX,Metacarpal_BBY,Metacarpal_BBZ,")
    fr.write("Metacarpal_BHX,Metacarpal_BHY,Metacarpal_BHZ,")
    fr.write("Metacarpal_BDirX,Metacarpal_BDirY,Metacarpal_BDirZ,")
    fr.write("Proximal_BBX,Proximal_BBY,Proximal_BBZ,")
    fr.write("Proximal_BHX,Proximal_BHY,Proximal_BHZ,")
    fr.write("Proximal_BDirX,Proximal_BDirY,Proximal_BDirZ,")
    fr.write("Intermediate_BBX,Intermediate_BBY,Intermediate_BBZ,")
    fr.write("Intermediate_BHX,Intermediate_BHY,Intermediate_BHZ,")
    fr.write("Intermediate_BDirX,Intermediate_BDirY,Intermediate_BDirZ,")
    fr.write("Distal_BBX,Distal_BBY,Distal_BBZ,")
    fr.write("Distal_BHX,Distal_BHY,Distal_BHZ,")
    fr.write("Distal_BDirX,Distal_BDirY,Distal_BDirZ\n")


    #get instance of background server
    server = Server(args.host_qtm, 8888)

    main()
    fl.close()
    fr.close()

    #get recorded intervall
    if not os.path.isdir("processed"):
        os.mkdir("processed")
    if not os.path.isdir("postProcessed"):
        os.mkdir("postProcessed")

    flp = open("processed/lefthandProcessed%s.txt" % countLeft, "w")
    with open("rawData/lefthand%s.txt" % countLeft, "r") as fl:
        try:
            flp.write(fl.readline())
        except StopIteration:
            print("No data for left hand!")
        for line in fl:
            recording = abs(np.fromstring(line, dtype=int, sep=','))[0]
            if recording:
                flp.write(line)
    flp.close()

    frp = open("processed/righthandProcessed%s.txt" % countRight, "w")
    with open("rawData/righthand%s.txt" % countRight, "r") as fr:
        try:
            frp.write(fr.readline())
        except StopIteration:
            print("No data for right hand!")
        for line in fr:
            recording = abs(np.fromstring(line, dtype=int, sep=','))[0]
            if recording:
                frp.write(line)
    frp.close()

    #sorting
    sortFingersByName(countLeft, countRight)
