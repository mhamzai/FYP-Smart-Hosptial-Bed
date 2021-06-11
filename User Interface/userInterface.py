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
from scipy.ndimage.filters import gaussian_filter
import copy


np.set_printoptions(threshold=sys.maxsize)


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
        self.bgImg = ImageTk.PhotoImage(
            Image.open(self.uiPath + 'alert.png').resize((1, 1)))
        self.bgOnCanvas = self.bg.create_image(
            0, 0, anchor=NW, image=self.bgImg)
        self.bg.create_text(int(self.cellSize*2.5), int(self.cellSize*1.125), fill='#ffffff',
                            font=(None, int(self.cellSize*0.35)), text='Pressure Map')
        self.bg.create_text(int(self.cellSize*7.25), int(self.cellSize*1.125),
                            fill='#ffffff', font=(None, int(self.cellSize*0.35)), text='Heat Map')
        self.bg.create_text(int(self.cellSize*11.125), int(self.cellSize*1.125),
                            fill='#ffffff', font=(None, int(self.cellSize*0.35)), text='Pulse')
        self.frame_1_1 = ttk.Frame(self.frame_1)
        self.pressureMap = tk.Canvas(self.frame_1_1)
        self.pressureMap.config(bg='#000000')
        self.pressureMap.place(anchor='nw', height=str(
            self.cellSize*8.25), width=str(self.cellSize*5.5), x='0', y='0')
        self.pressureMapImg = ImageTk.PhotoImage(
            Image.open(self.uiPath + 'alert.png').resize((1, 1)))
        self.pressureMapOnCanvas = self.pressureMap.create_image(
            0, 0, anchor=NW, image=self.pressureMapImg)
        self.frame_1_1.place(anchor='nw', height=str(self.cellSize*8.25), width=str(
            self.cellSize*5.5), x=str(self.cellSize*0.5), y=str(self.cellSize*1.5))
        self.frame_1_2_3_4_5_6_7 = ttk.Frame(self.frame_1)
        self.heatMap = tk.Canvas(self.frame_1_2_3_4_5_6_7)
        self.heatMap.config(bg='#000000')
        self.heatMap.place(anchor='nw', height=str(
            self.cellSize*5.25), width=str(self.cellSize*4), x='0', y='0')
        self.heatMapImg = ImageTk.PhotoImage(
            Image.open(self.uiPath + 'alert.png').resize((1, 1)))
        self.heatMapOnCanvas = self.heatMap.create_image(
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
            None, int(self.cellSize*0.625)))
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
            self.frame_1_2_3_4, font=(None, int(self.cellSize*0.625)))
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
            None, int(self.cellSize*0.625)))
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
        self.isOccupied = False
        alertText = ['', '', '']
        alertMode = False
        bagRemoved = False

        occupiedTone = sa.WaveObject.from_wave_file(
            self.uiPath + 'occupied.wav')
        unoccupiedTone = sa.WaveObject.from_wave_file(
            self.uiPath + 'unoccupied.wav')
        alertTone = sa.WaveObject.from_wave_file(self.uiPath + 'alert.wav')

        pressureMapArray = np.zeros((600, 400, 3), dtype='uint8')
        withoutPat = 0
        withPat = [0, 0, 0, 0]
        self.bedMat = np.zeros((80, 36))
        heatMapArray = np.ones((80, 36, 3), dtype='uint8') * 100
        x, y = np.ogrid[:80, :36]
        c1Mask = (x - 9)**2 + (y - 17)**2 <= 17**2
        c2Mask = (x - 12)**2 + (y - 17)**2 <= 17**2
        c3Mask = (x - 15)**2 + (y - 17)**2 <= 18**2
        self.bedMat[c1Mask] = 1
        self.bedMat[c2Mask] = 2
        self.bedMat[np.where(np.logical_and(
            c1Mask == True, c2Mask == True))] = 12
        self.bedMat[c3Mask] = 3
        self.bedMat[np.where(np.logical_and(
            c1Mask == True, c3Mask == True))] = 13
        self.bedMat[np.where(np.logical_and(
            c2Mask == True, c3Mask == True))] = 23
        self.bedMat[np.where(np.logical_and(np.logical_and(
            c1Mask == True, c2Mask == True), c3Mask == True))] = 123
        self.patTemp = [0, 0, 0]
        self.tempScale = 1.125

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

                self.pressureMap.image = None
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

                        if (self.isOccupied == True):
                            try:
                                if (not playUnoccupied.is_playing()):
                                    playUnoccupied = unoccupiedTone.play()
                            except:
                                playUnoccupied = unoccupiedTone.play()

                        self.isOccupied = False
                    else:
                        wt = str(round(wt)-5) + ' to ' + str(round(wt)+5)
                        self.weight.config(text=wt)
                        alertText[0] += 'Patient on bed' + '\n'

                        if (self.isOccupied == False):
                            try:
                                if (not playOccupied.is_playing()):
                                    playOccupied = occupiedTone.play()
                            except:
                                playOccupied = occupiedTone.play()

                        self.isOccupied = True

                        weightAlert = weightDict['msg']

                        if (weightAlert != '' and not weightAlert.startswith('Patient Moved after')):
                            alertText[0] += 'Patient hasn\'t been repositioned! Please do it.' + '\n'

                            try:
                                if (not playAlert.is_playing()):
                                    playAlert = alertTone.play()
                            except:
                                playAlert = alertTone.play()

                            alertMode = True

                    diffs = np.array(weightDict['diff']).astype(np.int)
                    activated = np.where(diffs > 24, 1, 0)
                    diffs = diffs.reshape(6, 4) * 2
                    resizedDiffs = copy.deepcopy(diffs)
                    resizedDiffs = resizedDiffs.repeat(
                        100, axis=0).repeat(100, axis=1)
                    pressureMapArray[:, :, 0] = np.clip(
                        gaussian_filter(resizedDiffs, sigma=32), 0, 255)
                    self.pressureMapImg = ImageTk.PhotoImage(Image.fromarray(pressureMapArray, 'RGB').resize(
                        (int(self.cellSize*5.5)+1, int(self.cellSize*8.25)+1), Image.ANTIALIAS))
                    self.pressureMap.itemconfig(
                        self.pressureMapOnCanvas, image=self.pressureMapImg)
                    self.pressureMap.image = self.pressureMapImg

            alertText[1] = ''

            if (self.tempDisconnected):
                alertText[1] += 'Temperature module disconnected!' + '\n'

                tp = '--'
                self.temperature.config(text=tp)

                self.heatMap.image = None
            elif (self.tempValue != ''):
                self.sensorBedMat = np.zeros((14, 4, 3))
                self.bedMatTemp = np.zeros((80, 36))

                msg = np.array(self.tempValue.split(","), dtype=float)

                if (not self.isOccupied):
                    tp = '--'
                    self.temperature.config(text=tp)

                    if (len(msg) == 1):
                        withoutPat = float(self.tempValue)
                elif (len(msg) == 4):
                    ambTemp = msg[0]
                    withPat = msg[1:]

                    sensorArea = 0
                    for i in range(0, 4):
                        if(activated[i]):
                            sensorArea += 121.5

                    for i in range(0, 8):
                        if(activated[i]):
                            if sensorArea == 0:
                                self.sensorBedMat[i//4][i % 4][0] = 1
                            else:
                                self.sensorBedMat[i//4][i % 4][0] = (
                                    withPat[0] - ((1-(sensorArea/(121.5*4))) * withoutPat)) / (sensorArea/(121.5*4))
                            self.patTemp[0] = self.sensorBedMat[i//4][i % 4][0]

                    sensorArea = 0
                    for i in range(0, 8):
                        if(activated[i]):
                            sensorArea += 121.5

                    for i in range(0, 8):
                        if(activated[i]):
                            if(i >= 4):
                                if sensorArea == 0:
                                    self.sensorBedMat[1][i-4][1] = 1
                                else:
                                    self.sensorBedMat[1][i-4][1] = (withPat[1] - (
                                        (1-(sensorArea/(121.5*4))) * withoutPat)) / (sensorArea/(121.5*4))
                                self.patTemp[1] = self.sensorBedMat[1][i-4][1]
                            else:
                                if sensorArea == 0:
                                    self.sensorBedMat[0][i][1] = 1
                                else:
                                    self.sensorBedMat[0][i][1] = (withPat[1] - (
                                        (1-(sensorArea/(121.5*4))) * withoutPat)) / (sensorArea/(121.5*4))
                                self.patTemp[1] = self.sensorBedMat[0][i][1]

                    sensorArea = 0
                    for i in range(0, 8):
                        if(activated[i]):
                            sensorArea += 121.5

                    for i in range(0, 8):
                        if(activated[i]):
                            if(i >= 4):
                                if sensorArea == 0:
                                    self.sensorBedMat[1][i-4][2] = 1
                                else:
                                    self.sensorBedMat[1][i-4][2] = (withPat[2] - (
                                        (1-(sensorArea/(121.5*4))) * withoutPat)) / (sensorArea/(121.5*4))
                                self.patTemp[2] = self.sensorBedMat[1][i-4][2]
                            else:
                                if sensorArea == 0:
                                    self.sensorBedMat[0][i][2] = 1
                                else:
                                    self.sensorBedMat[0][i][2] = (withPat[2] - (
                                        (1-(sensorArea/(121.5*4))) * withoutPat)) / (sensorArea/(121.5*4))
                                self.patTemp[2] = self.sensorBedMat[0][i][2]

                    for x in [0, 14]:
                        for y in [0, 9, 18, 27]:
                            self.FillMatrix(x, y, x//14, y//9, withoutPat)

                    tp = (self.patTemp[0] * 0.5) + (self.patTemp[1]
                                                    * 0.3) + (self.patTemp[2] * 0.2)
                    tp = str(round(tp*self.tempScale, 1))
                    self.temperature.config(text=tp)

                heatMapArray[:, :, 0] = np.clip(gaussian_filter(
                    self.bedMatTemp, sigma=3), 0, 360).astype(np.int)
                self.heatMapImg = ImageTk.PhotoImage(Image.fromarray(heatMapArray, 'HSV').resize(
                    (int(self.cellSize*4)+1, int(self.cellSize*4*2.22)+1), Image.ANTIALIAS))
                self.heatMap.itemconfig(
                    self.heatMapOnCanvas, image=self.heatMapImg)
                self.heatMap.image = self.heatMapImg

            alertText[2] = ''

            if (self.urineDisconnected):
                alertText[2] += 'Urine bag module disconnected!' + '\n'

                ub = '--'
                self.urinebag.config(text=ub)
            else:
                if (not self.isOccupied):
                    ub = '--'
                    self.urinebag.config(text=ub)
                else:
                    ub = self.urineBagValue
                    if (ub == '-1'):
                        ub = '--'
                        self.urinebag.config(text=ub)
                        alertText[2] += 'Urine Bag removed! Please attach one.' + '\n'

                        if (not bagRemoved):
                            try:
                                if (not playAlert.is_playing()):
                                    playAlert = alertTone.play()
                            except:
                                playAlert = alertTone.play()

                            alertMode = True

                        bagRemoved = True

                    else:
                        bagRemoved = False

                        if (ub == 'PP'):
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
                    serialWeight = serial.Serial('COM8')
                    self.weightDisconnected = False
                except:
                    self.weightDisconnected = True

                time.sleep(0.042)

    def updateTemp(self):
        self.tempDisconnected = True
        self.tempValue = ''

        while (True):
            try:
                if (self.isOccupied):
                    serialTemp.write(b'1')
                else:
                    serialTemp.write(b'0')

                self.tempValue = serialTemp.readline().decode().strip()
                print('Temperature Port:', self.tempValue)
            except:
                try:
                    serialTemp = serial.Serial('COM3')
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
                    serialUrineBag = serial.Serial('COM6')
                    self.urineDisconnected = False
                except:
                    self.urineDisconnected = True

                time.sleep(0.042)

    def FillMatrix(self, x, y, anchorX, anchorY, withoutPat):
        tempVal = self.sensorBedMat[anchorX][anchorY]

        for i in range(x, x+14):
            for j in range(y, y+9):
                if(self.bedMat[i][j] > 0):
                    if(tempVal.sum() > 0):
                        if (str(self.bedMat[i][j]).find('1') != -1):
                            self.bedMatTemp[i][j] += tempVal[0]

                        if (str(self.bedMat[i][j]).find('2') != -1):
                            self.bedMatTemp[i][j] += tempVal[1]

                        if (str(self.bedMat[i][j]).find('3') != -1):
                            self.bedMatTemp[i][j] += tempVal[2]

                        self.bedMatTemp[i][j] /= len(
                            str(int(self.bedMat[i][j])))
                        self.bedMatTemp[i][j] = self.bedMatTemp[i][j] * \
                            self.tempScale
                    else:
                        self.bedMatTemp[i][j] = withoutPat


if __name__ == '__main__':
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    app = smartBedUI(root)
    app.run()

    try:
        app.serialWeight.close()
    except:
        pass

    try:
        app.serialTemp.close()
    except:
        pass

    try:
        app.serialUrineBag.close()
    except:
        pass

    sys.exit()
