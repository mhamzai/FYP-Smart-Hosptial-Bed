import matplotlib.pyplot as plt
import numpy as np
import sys
import serial
import time


np.set_printoptions(threshold=sys.maxsize)




#hardcoding the bed matrix
bedMat = np.zeros((80, 36)) # 1 means circle is present, 0 means not present
x, y = np.ogrid[:80, :36]
c1Mask = (x - 9)**2 + (y - 17)**2 <= 17**2
c2Mask = (x - 12)**2 + (y - 17)**2 <= 17**2
c3Mask = (x - 15)**2 + (y - 17)**2 <= 18**2
#c4Mask = (x - 19)**2 + (y - 17)**2 <= 19**2
bedMat[c1Mask] = 1
bedMat[c2Mask] = 2
bedMat[np.where(np.logical_and(c1Mask == True,c2Mask == True))] = 12
bedMat[c3Mask] = 3
bedMat[np.where(np.logical_and(c1Mask == True,c3Mask == True))] = 13
bedMat[np.where(np.logical_and(c2Mask == True,c3Mask == True))] = 23
bedMat[np.where(np.logical_and(np.logical_and(c1Mask == True,c2Mask == True), c3Mask == True))] = 123


bedMatTemp = np.copy(bedMat)



#file = open("arr.txt", "w")
#for i in range(80):
#    for j in range(0, 36):
#        file.write(str(bedMat[i][j]))
#        file.write(" ")
#    file.write("\n")

#file.flush()
#file.close()


tempSensed = serial.Serial('COM6')


while 1:

    #msg =tempSensed.readline()
    #print(msg.decode())
    
    #if(tempSensed.readline().decode() == "1\n"):
    #    print("inside if\n")
    #    tempSensed.write(b'2')
    #else:
    #    print("inside else\n")
    #    continue

    msg = tempSensed.readline().decode()
    msg = np.array(msg.split(","), dtype=float)
    
    
    print(msg)

    for i in range(0, 80):
        for j in range(0, 36):

            if bedMat[i][j] == 1.0:
                bedMatTemp[i][j] = msg[0]        
            elif bedMat[i][j] == 2.0:
                bedMatTemp[i][j] = msg[1]
            elif bedMat[i][j] == 3.0:
                bedMatTemp[i][j] = msg[2]
            elif bedMat[i][j] == 12.0:
                bedMatTemp[i][j] = (msg[0] + msg[1])/2
            elif bedMat[i][j] == 13.0:
                bedMatTemp[i][j] = (msg[0] + msg[2])/2
            elif bedMat[i][j] == 23.0:
                bedMatTemp[i][j] = (msg[1] + msg[2])/2
            elif bedMat[i][j] == 123.0:
                bedMatTemp[i][j] = (msg[0] + msg[1] + msg[2])/3

    
    #file = open("arr.txt", "w")
    #for i in range(0, 80):
    #    for j in range(0, 36):
    #        file.write(str(bedMatTemp[i][j]))
    #        file.write(" ")
    #    file.write("\n")

    #file.flush()
    #file.close()
    

    plt.imshow(bedMatTemp)
    plt.show()

#credit goes to https://www.statology.org/matplotlib-circle/

#this creates an empty graph of bed's dimensions
plt.axis([-20, 80, -40, 100])
plt.axis("equal")

#defining circles
c1 = plt.Circle((17, 9), radius = 17, color = "red", alpha = 1) # 0 degree
c2 = plt.Circle((17, 11.9977), radius = 17.26, color = "orange", alpha = 0.7) # 5 degree
c3 = plt.Circle((17, 15.19), radius = 18.09, color = "yellow", alpha = 0.6) # 10 degree
c4 = plt.Circle((17, 18.815), radius = 19.63, color = "black", alpha = 0.4) # 15 degree
c5 = plt.Circle((17, 23.2645), radius = 22.1915, color = "blue", alpha = 0.3) # 20 degree
c6 = plt.Circle((17, 38.4499), radius = 33.9999, color = "green", alpha = 0.2) # 30 degree
bed = plt.Rectangle((0,0), 36, 80, color = "purple", alpha = 0.4) # bed visualization



#adding circles to the graph
#plt.gca().add_artist(c6)
#plt.gca().add_artist(c5)
#plt.gca().add_artist(c4)
plt.gca().add_artist(c3)
plt.gca().add_artist(c2)
plt.gca().add_artist(c1)
plt.gca().add_artist(bed)


#showing the graph
plt.show()

#plt.imshow(c1Mask)
#plt.imshow(c2Mask)
#plt.imshow(c3Mask)
#plt.imshow(c4Mask)
#plt.imshow(bedMat)
#plt.show()
#print(bedMat)
