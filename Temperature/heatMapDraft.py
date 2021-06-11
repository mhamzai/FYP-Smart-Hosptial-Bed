import matplotlib.pyplot as plt
import numpy as np
import sys
import serial
import time


# np.set_printoptions(threshold=sys.maxsize)


withoutPat = -1  # without patient temperature
withPat = -1  # with patient tempearature
sensorBedMat = ""


# hardcoding the bed matrix
bedMat = np.zeros((80, 36))  # 1 means circle is present, 0 means not present
x, y = np.ogrid[:80, :36]
c1Mask = (x - 9)**2 + (y - 17)**2 <= 17**2
c2Mask = (x - 12)**2 + (y - 17)**2 <= 17**2
c3Mask = (x - 15)**2 + (y - 17)**2 <= 18**2
#c4Mask = (x - 19)**2 + (y - 17)**2 <= 19**2
bedMat[c1Mask] = 1
bedMat[c2Mask] = 2
bedMat[np.where(np.logical_and(c1Mask == True, c2Mask == True))] = 12
bedMat[c3Mask] = 3
bedMat[np.where(np.logical_and(c1Mask == True, c3Mask == True))] = 13
bedMat[np.where(np.logical_and(c2Mask == True, c3Mask == True))] = 23
bedMat[np.where(np.logical_and(np.logical_and(
    c1Mask == True, c2Mask == True), c3Mask == True))] = 123


bedMatTemp = np.copy(bedMat)


def FillMatrix(x, y, anchorX, anchorY):

    tempVal = sensorBedMat[anchorX][anchorY]

    for i in range(x, x+14):
        for j in range(y, y+9):
            if(bedMat[i][j] == 0):
                bedMatTemp = tempVal


tempSensed = serial.Serial('COM6')

'''
Considering two rows of sensors. Each row contains four sensors.
The bed has 80 x 36 (inches) dimensions vertially and horizontally.
Giving each sensor an area of 13.5x9 inches square = 121.5 inches square.
Thus bed will be further visualized as 13.5 (~ 14) X 4 dimensions if seen
from perspective of sensor area.
'''


while 1:

    ###################################################################################################
    ###### 0 index gives temperature without patient, 1-3 gives three average temperatures ############
    ###### next 8 values give sensor activations ######################################################
    ###################################################################################################

    sensorBedMat = np.zeros((14, 4))  # sensor bed matrix

    msg = tempSensed.readline().decode()  # data received from IR sensor
    msg = np.array(msg.split(","), dtype=float)

    if not isOccupied:  # variable from Ammaar
        withoutPat = msg[1]  # without patient temperature
        continue
    else:
        withPat = msg[1:]  # with patient tempearature

    # for area 1 considering first row of sensors
    sensorArea = 0
    for i in range(0, 4):
        if(activations[i]):
            sensorArea += 121.5

    for i in range(0, 4):
        if(activations[i]):
            sensorBedMat[0][i] = (
                withPat[0] - ((1-(sensorArea/(121.5*4))) * withoutPat)) / (sensorArea/(121.5*4))

    # for area 2 considering 2 rows of sensors
    sensorArea = 0
    for i in range(0, 8):
        if(activations[i]):
            sensorArea += 121.5

    for i in range(0, 8):
        if(activations[i]):
            if(i >= 4):
                sensorBedMat[1][i-4] += (withPat[1] - ((1-(sensorArea/(121.5*4)))
                                         * withoutPat)) / (sensorArea/(121.5*4))
            else:
                sensorBedMat[0][i] += (withPat[1] - ((1-(sensorArea/(121.5*4)))
                                       * withoutPat)) / (sensorArea/(121.5*4))

    # for area 3 considering 2 rows of sensors
    sensorArea = 0
    for i in range(0, 8):
        if(activations[i]):
            sensorArea += 121.5

    for i in range(0, 8):
        if(activations[i]):
            if(i >= 4):
                sensorBedMat[1][i-4] += (withPat[2] - ((1-(sensorArea/(121.5*4)))
                                         * withoutPat)) / (sensorArea/(121.5*4))
            else:
                sensorBedMat[0][i] += (withPat[2] - ((1-(sensorArea/(121.5*4)))
                                       * withoutPat)) / (sensorArea/(121.5*4))

    for x in [0, 14]:
        for y in [0, 9, 18, 27]:

            FillMatrix(x, y, x/7, y/9)
