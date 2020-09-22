def sortFingersByName(countLeft, countRight):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']

    flpp = open("postProcessed/lefthandPostProcessed%s.txt" % countLeft, "w")
    with open("processed/lefthandProcessed%s.txt" % countLeft, "r") as flp:
        try:
            flpp.write(flp.readline())
        except StopIteration:
            print("No data for left hand!")
        for name in finger_names:
            for line in flp:
                if line.split(",")[18] == name:
                    flpp.write(line)
            flp.seek(0)

    frpp = open("postProcessed/righthandPostProcessed%s.txt" % countRight, "w")
    with open("processed/righthandProcessed%s.txt" % countRight, "r") as frp:
        try:
            frpp.write(frp.readline())
        except StopIteration:
            print("No data for right hand!")
        for name in finger_names:
            for line in frp:
                if line.split(",")[18] == name:
                    frpp.write(line)
            frp.seek(0)
