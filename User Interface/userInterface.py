import json
import os
import sys
import time
import tkinter as tk
import tkinter.ttk as ttk
from threading import *
from tkinter import *

import cv2
import numpy as np
import serial
import simpleaudio as sa
from PIL import Image, ImageTk


class smartBedUI:

    def __init__(self, master=None, firstInit=True):
        self.master = master
        self.frame_1 = ttk.Frame(self.master)
        self.windowWidth = self.master.winfo_width()
        self.windowHeight = self.master.winfo_height()
        self.cellSize = self.windowHeight / 10.75

        if (firstInit):
            self.uiPath = os.path.realpath(
                __file__).replace('userInterface.py', '')

        self.bg = tk.Canvas(self.frame_1)
        self.bg.config(bg='#000000')
        self.bg.place(anchor='nw', height=str(self.windowHeight),
                      width=str(self.windowWidth), x='0', y='0')
        self.bgImg = ImageTk.PhotoImage(Image.open(
            self.uiPath + 'bg.jpg').resize((self.windowWidth, self.windowHeight)))
        self.bgOnCanvas = self.bg.create_image(
            0, 0, anchor=NW, image=self.bgImg)
        self.bg.create_text(int(self.cellSize*2.5), int(self.cellSize*1.125), fill='#ffffff',
                            font=(None, int(self.cellSize*0.35)), text='Weight Distribution')
        self.bg.create_text(int(self.cellSize*7.25), int(self.cellSize*1.125),
                            fill='#ffffff', font=(None, int(self.cellSize*0.35)), text='Heat Map')
        self.bg.create_text(int(self.cellSize*11.125), int(self.cellSize*1.125),
                            fill='#ffffff', font=(None, int(self.cellSize*0.35)), text='Pulse')
        self.frame_1_1 = ttk.Frame(self.frame_1)

        self.contour = []
        y = 0
        index = 0
        for i in range(6):
            x = 0

            for j in range(4):
                self.contour.append(tk.Canvas(self.frame_1_1))
                self.contour[index].config(bg='#000000')
                self.contour[index].place(anchor='nw', height=str(
                    self.cellSize*1.375), width=str(self.cellSize*1.375), x=str(x), y=str(y))
                index += 1
                x += self.cellSize*1.375

            y += self.cellSize*1.375

        self.frame_1_1.place(anchor='nw', height=str(self.cellSize*8.25), width=str(
            self.cellSize*5.5), x=str(self.cellSize*0.5), y=str(self.cellSize*1.5))
        self.frame_1_2_3_4_5_6_7 = ttk.Frame(self.frame_1)
        self.heatMap = tk.Canvas(self.frame_1_2_3_4_5_6_7)
        self.heatMap.config(bg='#000000')
        self.heatMap.place(anchor='nw', height=str(
            self.cellSize*5.25), width=str(self.cellSize*4), x='0', y='0')
        self.heatMapImg = ImageTk.PhotoImage(
            Image.open(self.uiPath + 'alert.png').resize((1, 1)))
        self.mapOnCanvas = self.heatMap.create_image(
            0, 0, anchor=NW, image=self.heatMapImg)
        self.frame_1_2_3_4_5_6_7.place(anchor='nw', height=str(
            self.cellSize*5.25), width=str(self.cellSize*4), x=str(self.cellSize*6.25), y=str(self.cellSize*1.5))
        self.frame_1_2 = ttk.Frame(self.frame_1)
        self.canvas_1_1 = tk.Canvas(self.frame_1_2)
        self.canvas_1_1.config(bg='#000000')
        self.canvas_1_1.place(anchor='nw', height=str(
            self.cellSize*2.75), width=str(self.cellSize*8.25), x='0', y='0')
        self.frame_1_2.place(anchor='nw', height=str(self.cellSize*2.75), width=str(
            self.cellSize*8.25), x=str(self.cellSize*10.5), y=str(self.cellSize*1.5))
        self.frame_1_2_3 = ttk.Frame(self.frame_1)
        self.canvas_2_1 = tk.Canvas(self.frame_1_2_3)
        self.canvas_2_1.config(bg='#000000')
        self.canvas_2_1.place(anchor='nw', height=str(
            self.cellSize*2.25), width=str(self.cellSize*2.25), x='0', y='0')
        self.message_1 = tk.Label(
            self.frame_1_2_3, font=(None, int(self.cellSize*0.275)))
        self.message_1.config(bg='#000000', foreground='#00ff80', text='BPM')
        self.message_1.place(anchor='nw', height=str(self.cellSize*0.575), width=str(
            self.cellSize*1.125), x=str(self.cellSize*1.125), y=str(self.cellSize*1.625))
        self.heartrate = tk.Label(self.frame_1_2_3, font=(
            None, int(self.cellSize*0.8875)))
        self.heartrate.config(bg='#000000', foreground='#00ff80', text='--')
        self.heartrate.place(anchor='nw', height=str(self.cellSize), width=str(
            self.cellSize*2.25), x='0', y=str(self.cellSize*0.675))
        self.img2 = ImageTk.PhotoImage(Image.open(self.uiPath + 'pulse.png').resize(
            (int(self.cellSize*0.575)+1, int(self.cellSize*0.575)+1), Image.ANTIALIAS))
        self.canvas_2_1.create_image(
            self.cellSize*0.1, self.cellSize*0.1, anchor=NW, image=self.img2)
        self.frame_1_2_3.place(anchor='nw', height=str(self.cellSize*2.25), width=str(
            self.cellSize*2.25), x=str(self.cellSize*10.5), y=str(self.cellSize*4.5))
        self.frame_1_2_3_4 = ttk.Frame(self.frame_1)
        self.canvas_2_3 = tk.Canvas(self.frame_1_2_3_4)
        self.canvas_2_3.config(bg='#000000')
        self.canvas_2_3.place(anchor='nw', height=str(
            self.cellSize*2.25), width=str(self.cellSize*2.25), x='0', y='0')
        self.message_1_3 = tk.Label(
            self.frame_1_2_3_4, font=(None, int(self.cellSize*0.275)))
        self.message_1_3.config(bg='#000000', foreground='#ff0000', text='F')
        self.message_1_3.place(anchor='nw', height=str(self.cellSize*0.575), width=str(
            self.cellSize*0.575), x=str(self.cellSize*1.625), y=str(self.cellSize*1.625))
        self.temperature = tk.Label(
            self.frame_1_2_3_4, font=(None, int(self.cellSize*0.8875)))
        self.temperature.config(bg='#000000', foreground='#ff0000', text='--')
        self.temperature.place(anchor='nw', height=str(self.cellSize), width=str(
            self.cellSize*2.25), x='0', y=str(self.cellSize*0.675))
        self.img3 = ImageTk.PhotoImage(Image.open(self.uiPath + 'temp.png').resize(
            (int(self.cellSize*0.2875)+1, int(self.cellSize*0.575)+1), Image.ANTIALIAS))
        self.canvas_2_3.create_image(
            self.cellSize*0.1, self.cellSize*0.1, anchor=NW, image=self.img3)
        self.frame_1_2_3_4.place(anchor='nw', height=str(self.cellSize*2.25), width=str(
            self.cellSize*2.25), x=str(self.cellSize*13), y=str(self.cellSize*4.5))
        self.frame_1_2_3_4_5 = ttk.Frame(self.frame_1)
        self.canvas_2_4 = tk.Canvas(self.frame_1_2_3_4_5)
        self.canvas_2_4.config(bg='#000000')
        self.canvas_2_4.place(anchor='nw', height=str(
            self.cellSize*2.25), width=str(self.cellSize*3.25), x='0', y='0')
        self.message_1_4 = tk.Label(
            self.frame_1_2_3_4_5, font=(None, int(self.cellSize*0.275)))
        self.message_1_4.config(bg='#000000', foreground='#ff8040', text='KG')
        self.message_1_4.place(anchor='nw', height=str(self.cellSize*0.575), width=str(
            self.cellSize*0.575), x=str(self.cellSize*2.625), y=str(self.cellSize*1.625))
        self.weight = tk.Label(self.frame_1_2_3_4_5,
                               font=(None, int(self.cellSize*0.45)))
        self.weight.config(bg='#000000', foreground='#ff8040', text='-- to --')
        self.weight.place(anchor='nw', height=str(self.cellSize), width=str(
            self.cellSize*3.25), x='0', y=str(self.cellSize*0.675))
        self.img4 = ImageTk.PhotoImage(Image.open(self.uiPath + 'weight.png').resize(
            (int(self.cellSize*0.575)+1, int(self.cellSize*0.575)+1), Image.ANTIALIAS))
        self.canvas_2_4.create_image(
            self.cellSize*0.1, self.cellSize*0.1, anchor=NW, image=self.img4)
        self.frame_1_2_3_4_5.place(anchor='nw', height=str(self.cellSize*2.25), width=str(
            self.cellSize*3.25), x=str(self.cellSize*15.5), y=str(self.cellSize*4.5))
        self.frame_1_2_3_4_5_6 = ttk.Frame(self.frame_1)
        self.canvas_2_5 = tk.Canvas(self.frame_1_2_3_4_5_6)
        self.canvas_2_5.config(bg='#000000')
        self.canvas_2_5.place(anchor='nw', height=str(
            self.cellSize*2.75), width=str(self.cellSize*2.25), x='0', y='0')
        self.message_1_5 = tk.Label(
            self.frame_1_2_3_4_5_6, font=(None, int(self.cellSize*0.275)))
        self.message_1_5.config(bg='#000000', foreground='#ffff00', text='%')
        self.message_1_5.place(anchor='nw', height=str(self.cellSize*0.575), width=str(
            self.cellSize*0.575), x=str(self.cellSize*1.625), y=str(self.cellSize*2))
        self.urinebag = tk.Label(self.frame_1_2_3_4_5_6, font=(
            None, int(self.cellSize*0.8875)))
        self.urinebag.config(bg='#000000', foreground='#ffff00', text='--')
        self.urinebag.place(anchor='nw', height=str(self.cellSize), width=str(
            self.cellSize*2.25), x='0', y=str(self.cellSize*0.875))
        self.img5 = ImageTk.PhotoImage(Image.open(self.uiPath + 'urineBag.png').resize(
            (int(self.cellSize*0.2875)+1, int(self.cellSize*0.575)+1), Image.ANTIALIAS))
        self.canvas_2_5.create_image(
            self.cellSize*0.1, self.cellSize*0.1, anchor=NW, image=self.img5)
        self.frame_1_2_3_4_5_6.place(anchor='nw', height=str(self.cellSize*2.75), width=str(
            self.cellSize*2.25), x=str(self.cellSize*16.5), y=str(self.cellSize*7))
        self.frame_1_2_7 = ttk.Frame(self.frame_1)
        self.canvas_6_1 = tk.Canvas(self.frame_1_2_7)
        self.canvas_6_1.config(bg='#000000')
        self.canvas_6_1.place(anchor='nw', height=str(
            self.cellSize*2.75), width=str(self.cellSize*10), x='0', y='0')
        self.alert = tk.Label(self.frame_1_2_7, font=(
            None, int(self.cellSize*0.35)))
        self.alert.config(bg='#000000', foreground='#ffffff',
                          text='Unoccupied')
        self.alert.place(anchor='nw', height=str(self.cellSize*2.625), width=str(
            self.cellSize*9.125), x=str(self.cellSize*0.725), y=str(self.cellSize*0.0475))
        self.img6 = ImageTk.PhotoImage(Image.open(self.uiPath + 'alert.png').resize(
            (int(self.cellSize*0.575)+1, int(self.cellSize*0.575)+1), Image.ANTIALIAS))
        self.canvas_6_1.create_image(
            self.cellSize*0.1, self.cellSize*0.1, anchor=NW, image=self.img6)
        self.frame_1_2_7.place(anchor='nw', height=str(self.cellSize*2.75), width=str(
            self.cellSize*10), x=str(self.cellSize*6.25), y=str(self.cellSize*7))
        self.frame_1.place(anchor='nw', height=str(
            self.windowHeight), width=str(self.windowWidth), x='0', y='0')

        self.mainwindow = self.frame_1

        if (firstInit):
            self.startup = sa.WaveObject.from_wave_file(
                self.uiPath + 'Startup.wav')
            self.startup.play()

            self.master.geometry(
                '{0}x{1}+0+0'.format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
            self.master.bind('<Configure>', self.onResize)

            self.weightThread = Thread(target=self.updateWeight)
            self.weightThread.daemon = True
            self.weightThread.start()
            self.tempThread = Thread(target=self.updateTemp)
            self.tempThread.daemon = True
            self.tempThread.start()
            self.urineBagThread = Thread(target=self.updateUrineBag)
            self.urineBagThread.daemon = True
            self.urineBagThread.start()
            self.updateThread = Thread(target=self.update)
            self.updateThread.daemon = True
            self.updateThread.start()

    def run(self):
        self.mainwindow.mainloop()

    def onResize(self, event):
        previousWidth = self.windowWidth
        previousHeight = self.windowHeight

        if (previousWidth != self.master.winfo_width() or previousHeight != self.master.winfo_height()):
            self.__init__(self.master, firstInit=False)

    def update(self):
        bgVid = 'bgMain.mp4'
        isOccupied = False
        alertText = ['', '', '']
        previousAlert = ['', '', '']
        alertMode = False

        occupiedTone = sa.WaveObject.from_wave_file(
            self.uiPath + 'occupied.wav')
        unoccupiedTone = sa.WaveObject.from_wave_file(
            self.uiPath + 'unoccupied.wav')
        alertTone = sa.WaveObject.from_wave_file(self.uiPath + 'alert.wav')

        bedMat = np.zeros((80, 36))
        heatMapArray = np.zeros(
            (bedMat.shape[0], bedMat.shape[1], 3), dtype='uint8')
        x, y = np.ogrid[:80, :36]
        c1Mask = (x - 9)**2 + (y - 17)**2 <= 17**2
        c2Mask = (x - 12)**2 + (y - 17)**2 <= 17**2
        c3Mask = (x - 15)**2 + (y - 17)**2 <= 18**2
        bedMat[c1Mask] = 1
        bedMat[c2Mask] = 2
        bedMat[c3Mask] = 3
        bedMat[np.where(np.logical_and(c1Mask == True, c2Mask == True))] = 12
        bedMat[np.where(np.logical_and(c1Mask == True, c3Mask == True))] = 13
        bedMat[np.where(np.logical_and(c2Mask == True, c3Mask == True))] = 23
        bedMat[np.where(np.logical_and(np.logical_and(
            c1Mask == True, c2Mask == True), c3Mask == True))] = 123

        while (True):
            try:
                if (bgVid == 'bgMain.mp4' and alertMode):
                    bgVid = 'bgWarn.mp4'
                    cap = cv2.VideoCapture(self.uiPath + bgVid)
                elif (bgVid == 'bgWarn.mp4' and not alertMode):
                    bgVid = 'bgMain.mp4'
                    cap = cv2.VideoCapture(self.uiPath + bgVid)
            except:
                pass

            try:
                _, frame = cap.read()
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                self.bgImg = ImageTk.PhotoImage(Image.fromarray(cv2image).resize(
                    (self.windowWidth, self.windowHeight), Image.ANTIALIAS))
                self.bg.itemconfig(self.bgOnCanvas, image=self.bgImg)
                self.bg.image = self.bgImg
            except:
                cap = cv2.VideoCapture(self.uiPath + bgVid)

            alertMode = False

            if (self.weightDisconnected):
                alertText[0] = ''
                alertText[0] += 'Weight module disconnected!' + '\n'

                wt = '-- to --'
                self.weight.config(text=wt)

                for i in range(24):
                    color = '#000000'
                    self.contour[i].config(bg=color)
            else:
                weightDict = self.weightJSON
                if (weightDict.startswith('{')):
                    alertText[0] = ''
                    weightDict = json.loads(weightDict)
                    wt = weightDict['weight']

                    if (wt == 0.00):
                        wt = '-- to --'
                        self.weight.config(text=wt)
                        alertText[0] += 'Unoccupied' + '\n'

                        if (not('Unoccupied' in previousAlert[0]) and isOccupied == True):
                            try:
                                if (not playUnoccupied.is_playing()):
                                    playUnoccupied = unoccupiedTone.play()
                            except:
                                playUnoccupied = unoccupiedTone.play()

                        isOccupied = False
                    else:
                        isOccupied = True
                        wt = str(round(wt)-5) + ' to ' + str(round(wt)+5)
                        self.weight.config(text=wt)
                        alertText[0] += 'Patient on bed' + '\n'

                        if (not('Patient on bed' in previousAlert[0])):
                            try:
                                if (not playOccupied.is_playing()):
                                    playOccupied = occupiedTone.play()
                            except:
                                playOccupied = occupiedTone.play()

                        weightAlert = weightDict['msg']

                        if (weightAlert != ''):
                            alertText[0] += 'Patient hasn\'t been repositioned! Please do it.' + '\n'

                            try:
                                if (not playAlert.is_playing()):
                                    playAlert = alertTone.play()
                            except:
                                playAlert = alertTone.play()

                            alertMode = True

                    diffs = weightDict['diff']

                    for i in range(24):
                        diff = int(float(diffs[i]) * 2)

                        if (diff < 0):
                            diff = 0

                        hexVal = hex(diff).lstrip('0x').rstrip('L')

                        if (len(hexVal) == 1):
                            hexVal = '0' + hexVal
                        elif (len(hexVal) == 3):
                            hexVal = 'ff'
                        elif (len(hexVal) == 0):
                            hexVal = '00'

                        color = '#' + hexVal + '0000'
                        self.contour[i].config(bg=color)

                    previousAlert[0] = alertText[0]

            alertText[1] = ''

            if (self.tempDisconnected):
                alertText[1] += 'Temperature module disconnected!' + '\n'

                tp = '--'
                self.temperature.config(text=tp)

                self.heatMap.image = None
            else:
                if (not isOccupied):
                    tp = '--'
                    self.temperature.config(text=tp)
                else:
                    msg = np.array(self.tempValue.split(','), dtype=float)

                    for i in range(bedMat.shape[0]):
                        for j in range(bedMat.shape[1]):

                            if (bedMat[i][j] == 1.0):
                                bedMat[i][j] = msg[0]
                            elif (bedMat[i][j] == 2.0):
                                bedMat[i][j] = msg[1]
                            elif (bedMat[i][j] == 3.0):
                                bedMat[i][j] = msg[2]
                            elif (bedMat[i][j] == 12.0):
                                bedMat[i][j] = (msg[0] + msg[1]) / 2
                            elif (bedMat[i][j] == 13.0):
                                bedMat[i][j] = (msg[0] + msg[2]) / 2
                            elif (bedMat[i][j] == 23.0):
                                bedMat[i][j] = (msg[1] + msg[2]) / 2
                            elif (bedMat[i][j] == 123.0):
                                bedMat[i][j] = (msg[0] + msg[1] + msg[2]) / 3

                    heatMapArray[:, :, 0] = (bedMat * 6).astype(int)
                    self.heatMapImg = ImageTk.PhotoImage(Image.fromarray(heatMapArray, 'RGB').resize(
                        (int(self.cellSize*4)+1, int(self.cellSize*4*2.22)+1), Image.ANTIALIAS))
                    self.heatMap.itemconfig(
                        self.mapOnCanvas, image=self.heatMapImg)
                    self.heatMap.image = self.heatMapImg

                previousAlert[1] = alertText[1]

            alertText[2] = ''

            if (self.urineDisconnected):
                alertText[2] += 'Urine bag module disconnected!' + '\n'

                ub = '--'
                self.urinebag.config(text=ub)
            else:
                if (not isOccupied):
                    ub = '--'
                    self.urinebag.config(text=ub)
                else:
                    ub = self.urineBagValue
                    if (ub == '-1'):
                        ub = '--'
                        self.urinebag.config(text=ub)
                        alertText[2] += 'Urine Bag removed! Please attach one.' + '\n'

                        if (not('Urine Bag removed! Please attach one.' in previousAlert[2])):
                            try:
                                if (not playAlert.is_playing()):
                                    playAlert = alertTone.play()
                            except:
                                playAlert = alertTone.play()

                            alertMode = True

                    elif (ub == 'PP'):
                        alertText[2] += 'Patient hasn\'t urinated in last 6 hours!' + '\n'

                        try:
                            if (not playAlert.is_playing()):
                                playAlert = alertTone.play()
                        except:
                            playAlert = alertTone.play()

                        alertMode = True

                    elif (ub.isnumeric()):
                        self.urinebag.config(text=ub)

                        if (ub == '100'):
                            alertText[2] += 'Urine Bag full! Please change it ASAP.' + '\n'

                            try:
                                if (not playAlert.is_playing()):
                                    playAlert = alertTone.play()
                            except:
                                playAlert = alertTone.play()

                            alertMode = True

                        elif (int(float(ub)) > 80):
                            alertText[2] += 'Urine Bag almost full! Please drain / change it.' + '\n'

                            try:
                                if (not playAlert.is_playing()):
                                    playAlert = alertTone.play()
                            except:
                                playAlert = alertTone.play()

                            alertMode = True

            previousAlert[2] = alertText[2]

            combinedAlert = alertText[0] + alertText[1] + alertText[2]
            combinedAlert = combinedAlert.rstrip('\n')
            self.alert.config(text=combinedAlert)

            time.sleep(0.042)

    def updateWeight(self):
        self.weightDisconnected = True
        self.weightJSON = ''

        while (True):
            try:
                self.weightJSON = serialWeight.readline().decode().strip()
                print('Weight Port:', self.weightJSON)
            except:
                try:
                    serialWeight = serial.Serial('COM4')
                    self.weightDisconnected = False
                except:
                    self.weightDisconnected = True

                time.sleep(0.042)

    def updateTemp(self):
        self.tempDisconnected = True
        self.tempValue = ''

        while (True):
            try:
                self.tempValue = serialTemp.readline().decode().strip()
                print('Temperature Port:', self.tempValue)
            except:
                try:
                    serialTemp = serial.Serial('COM5')
                    self.tempDisconnected = False
                except:
                    self.tempDisconnected = True

                time.sleep(0.042)

    def updateUrineBag(self):
        self.urineDisconnected = True
        self.urineBagValue = ''

        while (True):
            try:
                self.urineBagValue = serialUrineBag.readline().decode().strip()
                print('Urine Bag Port:', self.urineBagValue)
            except:
                try:
                    serialUrineBag = serial.Serial('COM7')
                    self.urineDisconnected = False
                except:
                    self.urineDisconnected = True

                time.sleep(0.042)


if __name__ == '__main__':
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    app = smartBedUI(root)
    app.run()
    sys.exit()
