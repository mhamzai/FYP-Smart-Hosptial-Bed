import json
import os
import sys
import time
import tkinter as tk
import tkinter.ttk as ttk
from datetime import datetime
from threading import *
from tkinter import *

import cv2
import numpy as np
import serial
import simpleaudio as sa
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from PIL import Image, ImageTk
from scipy.ndimage import measurements
from scipy.ndimage.filters import gaussian_filter

np.set_printoptions(threshold=sys.maxsize)


class smartBedUI:

    def __init__(self, master=None, firstInit=True):
        if (firstInit):
            self.uiPath = os.path.realpath(
                __file__).replace('userInterface.py', '')

        self.master = master
        self.frameBg = ttk.Frame(self.master)
        self.windowWidth = self.master.winfo_width()
        self.windowHeight = self.master.winfo_height()
        self.bg = tk.Canvas(self.frameBg)
        self.bg.config(bg='#000000')
        self.bg.place(anchor='nw', height=str(self.windowHeight),
                      width=str(self.windowWidth), x='0', y='0')
        self.imageBg = ImageTk.PhotoImage(Image.open(
            self.uiPath + 'alert.png').resize((1, 1)))
        self.bgOnCanvas = self.bg.create_image(
            0, 0, anchor=NW, image=self.imageBg)
        self.bg.create_text(int(self.windowWidth/11), int(self.windowHeight/9.25), fill='#ffffff',
                            font=(None, int((self.windowWidth+self.windowHeight)/100)), text='Pressure Map')
        self.bg.create_text(int(self.windowWidth/2.7), int(self.windowHeight/9.25), fill='#ffffff',
                            font=(None, int((self.windowWidth+self.windowHeight)/100)), text='Heat Map')
        self.bg.create_text(int(self.windowWidth/1.741), int(self.windowHeight/9.25), fill='#ffffff',
                            font=(None, int((self.windowWidth+self.windowHeight)/100)), text='Pulse')
        self.framePMap = ttk.Frame(self.frameBg)
        self.pressureMap = tk.Canvas(self.framePMap)
        self.pressureMap.config(bg='#000000')
        self.pressureMap.place(anchor='nw', height=str(
            int(self.windowHeight/1.3)), width=str(int(self.windowWidth/3.5)), x='0', y='0')
        self.pressureMapImg = ImageTk.PhotoImage(
            Image.open(self.uiPath + 'alert.png').resize((1, 1)))
        self.pMapOnCanvas = self.pressureMap.create_image(
            0, 0, anchor=NW, image=self.pressureMapImg)
        self.framePMap.place(anchor='nw', height=str(int(self.windowHeight/1.3)), width=str(int(
            self.windowWidth/3.5)), x=str(int(self.windowWidth/35)), y=str(int(self.windowHeight/7.25)))
        self.frameHMap = ttk.Frame(self.frameBg)
        self.heatMap = tk.Canvas(self.frameHMap)
        self.heatMap.config(bg='#000000')
        self.heatMap.place(anchor='nw', height=str(
            int(self.windowHeight/2.05)), width=str(int(self.windowWidth/4.75)), x='0', y='0')
        self.heatMapImg = ImageTk.PhotoImage(
            Image.open(self.uiPath + 'alert.png').resize((1, 1)))
        self.hMapOnCanvas = self.heatMap.create_image(
            0, 0, anchor=NW, image=self.heatMapImg)
        self.frameHMap.place(anchor='nw', height=str(int(self.windowHeight/2.05)), width=str(
            int(self.windowWidth/4.75)), x=str(int(self.windowWidth/3.06)), y=str(int(self.windowHeight/7.25)))
        self.framePulsePlot = ttk.Frame(self.frameBg)
        self.canvasPulsePlot = tk.Canvas(self.framePulsePlot)
        self.canvasPulsePlot.config(bg='#000000')
        self.canvasPulsePlot.place(anchor='nw', height=str(
            int(self.windowHeight/3.9)), width=str(int(self.windowWidth/2.35)), x='0', y='0')
        self.framePulsePlot.place(anchor='nw', height=str(int(self.windowHeight/3.9)), width=str(int(
            self.windowWidth/2.35)), x=str(int(self.windowWidth/1.82)), y=str(int(self.windowHeight/7.25)))
        self.framePulse = ttk.Frame(self.frameBg)
        self.canvasPulse = tk.Canvas(self.framePulse)
        self.canvasPulse.config(bg='#000000')
        self.canvasPulse.place(anchor='nw', height=str(
            int(self.windowHeight/4.832)), width=str(int(self.windowWidth/8.5)), x='0', y='0')
        self.labelPulseUnit = tk.Label(self.framePulse, font=(
            None, int((self.windowWidth+self.windowHeight)/125)))
        self.labelPulseUnit.config(
            bg='#000000', foreground='#00ff80', text='BPM')
        self.labelPulseUnit.place(anchor='nw', height=str(int(self.windowHeight/30)), width=str(int(
            self.windowWidth/23)), x=str(int(self.windowWidth/15)), y=str(int(self.windowHeight/6.05)))
        labelPulse = tk.Label(self.framePulse, font=(
            None, int((self.windowWidth+self.windowHeight)/50)))
        labelPulse.config(bg='#000000', foreground='#00ff80', text='--')
        labelPulse.place(anchor='nw', height=str(int(self.windowHeight/10)), width=str(
            int(self.windowWidth/8.5)), x='0', y=str(int(self.windowHeight/17.5)))
        self.imagePulse = ImageTk.PhotoImage(Image.open(self.uiPath + 'pulse.png').resize(
            (int((self.windowWidth+self.windowHeight)/65)+1, int((self.windowWidth+self.windowHeight)/65)+1), Image.ANTIALIAS))
        self.canvasPulse.create_image(
            int(self.windowWidth/225), int(self.windowHeight/125), anchor=NW, image=self.imagePulse)
        self.framePulse.place(anchor='nw', height=str(int(self.windowHeight/4.832)), width=str(int(
            self.windowWidth/8.5)), x=str(int(self.windowWidth/1.82)), y=str(int(self.windowHeight/2.39)))
        self.frameTemp = ttk.Frame(self.frameBg)
        self.canvasTemp = tk.Canvas(self.frameTemp)
        self.canvasTemp.config(bg='#000000')
        self.canvasTemp.place(anchor='nw', height=str(
            int(self.windowHeight/4.832)), width=str(int(self.windowWidth/8.5)), x='0', y='0')
        self.canvasTempUnit = tk.Label(self.frameTemp, font=(
            None, int((self.windowWidth+self.windowHeight)/125)))
        self.canvasTempUnit.config(
            bg='#000000', foreground='#ff0000', text='F')
        self.canvasTempUnit.place(anchor='nw', height=str(int(self.windowHeight/30)), width=str(int(
            self.windowWidth/50)), x=str(int(self.windowWidth/11)), y=str(int(self.windowHeight/6.05)))
        self.labelTemp = tk.Label(self.frameTemp, font=(
            None, int((self.windowWidth+self.windowHeight)/50)))
        self.labelTemp.config(bg='#000000', foreground='#ff0000', text='--')
        self.labelTemp.place(anchor='nw', height=str(int(self.windowHeight/10)),
                             width=str(int(self.windowWidth/8.5)), x='0', y=str(self.windowHeight/17.5))
        self.imageTemp = ImageTk.PhotoImage(Image.open(self.uiPath + 'temp.png').resize(
            (int((self.windowWidth+self.windowHeight)/65)+1, int((self.windowWidth+self.windowHeight)/65)+1), Image.ANTIALIAS))
        self.canvasTemp.create_image(
            int(self.windowWidth/225), int(self.windowHeight/125), anchor=NW, image=self.imageTemp)
        self.frameTemp.place(anchor='nw', height=str(int(self.windowHeight/4.832)), width=str(int(
            self.windowWidth/8.5)), x=str(int(self.windowWidth/1.47)), y=str(int(self.windowHeight/2.39)))
        self.frameWeight = ttk.Frame(self.frameBg)
        self.canvasWeight = tk.Canvas(self.frameWeight)
        self.canvasWeight.config(bg='#000000')
        self.canvasWeight.place(anchor='nw', height=str(
            int(self.windowHeight/4.832)), width=str(int(self.windowWidth/6.1)), x='0', y='0')
        self.labelWeightUnit = tk.Label(self.frameWeight, font=(
            None, int((self.windowWidth+self.windowHeight)/125)))
        self.labelWeightUnit.config(
            bg='#000000', foreground='#ff8040', text='KG')
        self.labelWeightUnit.place(anchor='nw', height=str(int(self.windowHeight/30)), width=str(int(
            self.windowWidth/32)), x=str(int(self.windowWidth/8)), y=str(int(self.windowHeight/6.05)))
        self.labelWeight = tk.Label(self.frameWeight, font=(
            None, int((self.windowWidth+self.windowHeight)/65)))
        self.labelWeight.config(
            bg='#000000', foreground='#ff8040', text='-- to --')
        self.labelWeight.place(anchor='nw', height=str(int(self.windowHeight/10)), width=str(
            int(self.windowWidth/6.1)), x='0', y=str(int(self.windowHeight/17.5)))
        self.imageWeight = ImageTk.PhotoImage(Image.open(self.uiPath + 'weight.png').resize(
            (int((self.windowWidth+self.windowHeight)/65)+1, int((self.windowWidth+self.windowHeight)/65)+1), Image.ANTIALIAS))
        self.canvasWeight.create_image(
            int(self.windowWidth/225), int(self.windowHeight/125), anchor=NW, image=self.imageWeight)
        self.frameWeight.place(anchor='nw', height=str(int(self.windowHeight/4.832)), width=str(
            int(self.windowWidth/6.1)), x=str(int(self.windowWidth/1.233)), y=str(int(self.windowHeight/2.39)))
        self.frameUBag = ttk.Frame(self.frameBg)
        self.canvasUBag = tk.Canvas(self.frameUBag)
        self.canvasUBag.config(bg='#000000')
        self.canvasUBag.place(anchor='nw', height=str(
            int(self.windowHeight/3.92)), width=str(int(self.windowWidth/8.5)), x='0', y='0')
        self.labelUBagUnit = tk.Label(self.frameUBag, font=(
            None, int((self.windowWidth+self.windowHeight)/125)))
        self.labelUBagUnit.config(bg='#000000', foreground='#ffff00', text='%')
        self.labelUBagUnit.place(anchor='nw', height=str(int(self.windowHeight/22.5)), width=str(int(
            self.windowWidth/42.5)), x=str(int(self.windowWidth/11.5)), y=str(int(self.windowHeight/5.15)))
        self.urinebag = tk.Label(self.frameUBag, font=(
            None, int((self.windowWidth+self.windowHeight)/50)))
        self.urinebag.config(bg='#000000', foreground='#ffff00', text='--')
        self.urinebag.place(anchor='nw', height=str(int(self.windowHeight/10)), width=str(
            int(self.windowWidth/8.5)), x='0', y=str(int(self.windowHeight/12.5)))
        self.imageUBag = ImageTk.PhotoImage(Image.open(self.uiPath + 'urineBag.png').resize(
            (int((self.windowWidth+self.windowHeight)/65)+1, int((self.windowWidth+self.windowHeight)/65)+1), Image.ANTIALIAS))
        self.canvasUBag.create_image(
            int(self.windowWidth/225), int(self.windowHeight/125), anchor=NW, image=self.imageUBag)
        self.frameUBag.place(anchor='nw', height=str(int(self.windowHeight/3.92)), width=str(
            int(self.windowWidth/8.5)), x=str(int(self.windowWidth/1.166)), y=str(int(self.windowHeight/1.537)))
        self.frameAlert = ttk.Frame(self.frameBg)
        self.canvasAlert = tk.Canvas(self.frameAlert)
        self.canvasAlert.config(bg='#000000')
        self.canvasAlert.place(anchor='nw', height=str(
            int(self.windowHeight/3.92)), width=str(int(self.windowWidth/1.93)), x='0', y='0')
        self.labelAlert = tk.Label(self.frameAlert, font=(
            None, int((self.windowWidth+self.windowHeight)/113)))
        self.labelAlert.config(bg='#000000', foreground='#ffffff',
                               text='Unoccupied')
        self.labelAlert.place(anchor='nw', height=str(int(self.windowHeight/4.01)), width=str(int(
            self.windowWidth/2.06)), x=str(int(self.windowWidth/32.5)), y=str(int(self.windowHeight/375)))
        self.imageAlert = ImageTk.PhotoImage(Image.open(self.uiPath + 'alert.png').resize(
            (int((self.windowWidth+self.windowHeight)/65)+1, int((self.windowWidth+self.windowHeight)/65)+1), Image.ANTIALIAS))
        self.canvasAlert.create_image(
            int(self.windowWidth/225), int(self.windowHeight/125), anchor=NW, image=self.imageAlert)
        self.frameAlert.place(anchor='nw', height=str(int(self.windowHeight/3.92)), width=str(int(
            self.windowWidth/1.93)), x=str(int(self.windowWidth/3.06)), y=str(int(self.windowHeight/1.537)))
        self.frameBg.place(anchor='nw', height=str(
            self.windowHeight), width=str(self.windowWidth), x='0', y='0')

        self.mainwindow = self.frameBg

        if (firstInit):
            self.startup = sa.WaveObject.from_wave_file(
                self.uiPath + 'Startup.wav')
            self.startup.play()

            self.master.geometry(
                '{0}x{1}+0+0'.format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
            self.master.bind('<Configure>', self.onResize)

            self.influxdbThread = Thread(target=self.influxdb)
            self.influxdbThread.daemon = True
            self.influxdbThread.start()
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
            self.grafanaThread = Thread(target=self.grafana)
            self.grafanaThread.daemon = True
            self.grafanaThread.start()

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
        pressureMapArray = np.zeros((600, 400, 3), dtype='uint8')
        alertText = ['', '', '']
        alertMode = False
        ubRemoved = False
        weightList = []
        tempList = []
        ubList = []
        self.withoutPat = 0
        withPat = [0, 0, 0, 0]
        self.bedMat = np.zeros((80, 36))
        heatMapArray = np.ones((80, 36, 3), dtype='uint8') * 255
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
        occupiedTone = sa.WaveObject.from_wave_file(
            self.uiPath + 'occupied.wav')
        unoccupiedTone = sa.WaveObject.from_wave_file(
            self.uiPath + 'unoccupied.wav')
        alertTone = sa.WaveObject.from_wave_file(self.uiPath + 'alert.wav')
        lastUBPercent = -1
        unturnedTime = 0

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
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.imageBg = ImageTk.PhotoImage(Image.fromarray(cv2image).resize(
                    (self.windowWidth, self.windowHeight), Image.ANTIALIAS))
                self.bg.itemconfig(self.bgOnCanvas, image=self.imageBg)
                self.bg.image = self.imageBg
            except:
                cap = cv2.VideoCapture(self.uiPath + bgVid)

            alertMode = False

            if (self.weightDisconnected):
                unturnedTimeStart = time.time()
                time.perf_counter()

                alertText[0] = ''
                alertText[0] += 'Body detection module disconnected!' + '\n'
                self.isOccupied = False

                wt = '-- to --'
                self.labelWeight.config(text=wt)
                weightList = []

                self.pressureMapImg = ImageTk.PhotoImage(
                    Image.open(self.uiPath + 'alert.png').resize((1, 1)))
                self.pressureMap.itemconfig(
                    self.pMapOnCanvas, image=self.pressureMapImg)
                self.pressureMap.image = self.pressureMapImg
            else:
                weightDict = self.weightJSON

                if (weightDict.startswith('{')):
                    alertText[0] = ''
                    weightDict = json.loads(weightDict)
                    wt = weightDict['weight']

                    if (wt == 0.00):
                        if (self.isOccupied == True and int(unturnedTime) > 0):
                            self.writeToDb(
                                'patient_turn_intervals', int(unturnedTime))

                            try:
                                if (not playUnoccupied.is_playing()):
                                    playUnoccupied = unoccupiedTone.play()
                            except:
                                playUnoccupied = unoccupiedTone.play()

                        unturnedTimeStart = time.time()
                        time.perf_counter()

                        wt = '-- to --'
                        self.labelWeight.config(text=wt)
                        weightList = []
                        alertText[0] += 'Unoccupied' + '\n'

                        self.isOccupied = False
                    else:
                        weightList.append(wt)

                        if (len(weightList) > 8):
                            weightList.pop(0)

                        wt = self.avg(weightList)
                        wt = str(wt-5) + ' to ' + str(wt+5)
                        self.labelWeight.config(text=wt)
                        alertText[0] += 'Patient on bed' + '\n'

                        if (self.isOccupied == False):
                            try:
                                if (not playOccupied.is_playing()):
                                    playOccupied = occupiedTone.play()
                            except:
                                playOccupied = occupiedTone.play()
                        else:
                            unturnedTime = time.time() - unturnedTimeStart

                        self.isOccupied = True
                        weightAlert = weightDict['msg']

                        if (weightAlert.startswith('Patient not Turned')):
                            alertText[0] += 'Patient hasn\'t been repositioned! Please do it.' + '\n'

                            try:
                                if (not playAlert.is_playing()):
                                    playAlert = alertTone.play()
                            except:
                                playAlert = alertTone.play()

                            alertMode = True
                        elif (weightAlert.startswith('Patient Moved')):
                            if (int(unturnedTime) > 0):
                                self.writeToDb(
                                    'patient_turn_intervals', int(unturnedTime))

                            unturnedTimeStart = time.time()
                            time.perf_counter()

                    diffs = np.array(weightDict['diff']).astype(np.int)
                    activated = np.where(diffs > 24, 1, 0)
                    pressureMapArray[:, :, 0] = np.clip(gaussian_filter((diffs.reshape(
                        6, 4) * 2).repeat(100, axis=0).repeat(100, axis=1), sigma=32), 0, 255)
                    self.pressureMapImg = ImageTk.PhotoImage(Image.fromarray(pressureMapArray, 'RGB').resize(
                        (int(self.windowWidth/3.5)+1, int(self.windowHeight/1.3)+1), Image.ANTIALIAS))
                    self.pressureMap.itemconfig(
                        self.pMapOnCanvas, image=self.pressureMapImg)
                    self.pressureMap.image = self.pressureMapImg

            alertText[1] = ''

            if (self.tempDisconnected):
                alertText[1] += 'Temperature module disconnected!' + '\n'

                self.labelTemp.config(text='--')
                tempList = []

                self.heatMapImg = ImageTk.PhotoImage(
                    Image.open(self.uiPath + 'alert.png').resize((1, 1)))
                self.heatMap.itemconfig(
                    self.hMapOnCanvas, image=self.heatMapImg)
                self.heatMap.image = self.heatMapImg
            elif (self.tempValue != ''):
                self.sensorBedMat = np.zeros((14, 4, 3))
                self.bedMatTemp = np.zeros((80, 36))

                msg = np.array(self.tempValue.split(','), dtype=float)

                if (not self.isOccupied):
                    self.labelTemp.config(text='--')
                    tempList = []

                    if (len(msg) == 1):
                        self.withoutPat = float(self.tempValue)
                elif (len(msg) == 4):
                    ambTemp = msg[0]
                    withPat = msg[1:]

                    sensorArea = 0
                    for i in range(0, 4):
                        if (activated[i]):
                            sensorArea += 121.5

                    for i in range(0, 8):
                        if (activated[i]):
                            if (sensorArea == 0):
                                self.sensorBedMat[i//4][i % 4][0] = 1
                            else:
                                self.sensorBedMat[i//4][i % 4][0] = (
                                    withPat[0] - ((1-(sensorArea/(121.5*4))) * self.withoutPat)) / (sensorArea/(121.5*4))
                            self.patTemp[0] = self.sensorBedMat[i//4][i % 4][0]

                    sensorArea = 0
                    for i in range(0, 8):
                        if (activated[i]):
                            sensorArea += 121.5

                    for i in range(0, 8):
                        if (activated[i]):
                            if (i >= 4):
                                if (sensorArea == 0):
                                    self.sensorBedMat[1][i-4][1] = 1
                                else:
                                    self.sensorBedMat[1][i-4][1] = (withPat[1] - (
                                        (1-(sensorArea/(121.5*4))) * self.withoutPat)) / (sensorArea/(121.5*4))
                                self.patTemp[1] = self.sensorBedMat[1][i-4][1]
                            else:
                                if (sensorArea == 0):
                                    self.sensorBedMat[0][i][1] = 1
                                else:
                                    self.sensorBedMat[0][i][1] = (withPat[1] - (
                                        (1-(sensorArea/(121.5*4))) * self.withoutPat)) / (sensorArea/(121.5*4))
                                self.patTemp[1] = self.sensorBedMat[0][i][1]

                    sensorArea = 0
                    for i in range(0, 8):
                        if (activated[i]):
                            sensorArea += 121.5

                    for i in range(0, 8):
                        if (activated[i]):
                            if (i >= 4):
                                if (sensorArea == 0):
                                    self.sensorBedMat[1][i-4][2] = 1
                                else:
                                    self.sensorBedMat[1][i-4][2] = (withPat[2] - (
                                        (1-(sensorArea/(121.5*4))) * self.withoutPat)) / (sensorArea/(121.5*4))
                                self.patTemp[2] = self.sensorBedMat[1][i-4][2]
                            else:
                                if (sensorArea == 0):
                                    self.sensorBedMat[0][i][2] = 1
                                else:
                                    self.sensorBedMat[0][i][2] = (withPat[2] - (
                                        (1-(sensorArea/(121.5*4))) * self.withoutPat)) / (sensorArea/(121.5*4))
                                self.patTemp[2] = self.sensorBedMat[0][i][2]

                    for x in [0, 14]:
                        for y in [0, 9, 18, 27]:
                            self.FillMatrix(x, y, x//14, y//9)

                    tp = int(((self.patTemp[0] * 0.5) + (self.patTemp[1]
                             * 0.3) + (self.patTemp[2] * 0.2)) * self.tempScale)
                    tempList.append(tp)

                    if (len(tempList) > 32):
                        tempList.pop(0)

                    tp = self.avg(tempList)
                    self.labelTemp.config(text=str(tp))

                heatMapArray[:, :, 0] = np.clip(gaussian_filter(
                    115-self.bedMatTemp, sigma=2), 0, 179).astype(np.int)
                self.heatMapImg = ImageTk.PhotoImage(Image.fromarray(heatMapArray, 'HSV').resize(
                    (int(self.windowWidth/4.75)+1, int(self.windowHeight/2.05)+1), Image.ANTIALIAS))
                self.heatMap.itemconfig(
                    self.hMapOnCanvas, image=self.heatMapImg)
                self.heatMap.image = self.heatMapImg

            alertText[2] = ''

            if (self.urineDisconnected):
                alertText[2] += 'Urine bag module disconnected!' + '\n'

                self.urinebag.config(text='--')
                ubPercent = -1
                ubList = []

                if (self.isOccupied and ubPercent != lastUBPercent):
                    self.writeToDb('urine_bag_fill_percentage', ubPercent)

                lastUBPercent = ubPercent
            else:
                ub = self.urineBagValue

                if (ub == '-1'):
                    self.urinebag.config(text='--')
                    alertText[2] += 'Urine Bag removed! Please attach one.' + '\n'
                    ubPercent = int(ub)

                    if (self.isOccupied and ubPercent != lastUBPercent):
                        self.writeToDb('urine_bag_fill_percentage', ubPercent)

                    lastUBPercent = ubPercent

                    if (not ubRemoved):
                        try:
                            if (not playAlert.is_playing()):
                                playAlert = alertTone.play()
                        except:
                            playAlert = alertTone.play()

                        alertMode = True

                    ubRemoved = True
                else:
                    ubRemoved = False

                    if (ub.isnumeric()):
                        ubPercent = int(ub)
                        ubList.append(ubPercent)

                        if (len(ubList) > 32):
                            ubList.pop(0)

                        ubPercent = self.avg(ubList)
                        self.urinebag.config(text=str(ubPercent))

                        if (self.isOccupied and ubPercent != lastUBPercent):
                            self.writeToDb(
                                'urine_bag_fill_percentage', ubPercent)

                        lastUBPercent = ubPercent

                        if (ubPercent == 100):
                            alertText[2] += 'Urine Bag full! Please change it ASAP.' + '\n'

                            try:
                                if (not playAlert.is_playing()):
                                    playAlert = alertTone.play()
                            except:
                                playAlert = alertTone.play()

                            alertMode = True

                        elif (ubPercent > 80):
                            alertText[2] += 'Urine Bag almost full! Please drain / change it.' + '\n'

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

            combinedAlert = alertText[0] + alertText[1] + alertText[2]
            combinedAlert = combinedAlert.rstrip('\n')
            self.labelAlert.config(text=combinedAlert)

            time.sleep(0.042)

    def updateWeight(self):
        self.weightDisconnected = True
        self.weightJSON = ''

        while (True):
            try:
                self.weightJSON = serialWeight.readline().decode().strip()
                print('Body Detection Port:', self.weightJSON)
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

    def avg(self, lst):
        return round(sum(lst)/len(lst))

    def FillMatrix(self, x, y, anchorX, anchorY):
        tempVal = self.sensorBedMat[anchorX][anchorY]

        for i in range(x, x+14):
            for j in range(y, y+9):
                if (self.bedMat[i][j] > 0):
                    if (tempVal.sum() > 0):
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
                        self.bedMatTemp[i][j] = self.withoutPat

    def influxdb(self):
        os.system(self.uiPath + 'influxdb\\influxdb2-2.0.7-windows-amd64\\influxd')

    def grafana(self):
        os.system(self.uiPath + 'grafana\\grafana\\bin\\grafana-server -homepath "' +
                  self.uiPath + 'grafana\\grafana"')

    def writeToDb(self, measurement, fieldValue):
        if (measurement == 'patient_turn_intervals'):
            fieldKey = 'Seconds since last turn'
        elif (measurement == 'urine_bag_fill_percentage'):
            fieldKey = 'Percentage filled'

        try:
            token = "s0WZ_6Gga4ybJxmWpICLlxlMe5N6acqbsL05SxSoekojleg4Rlzee0uKg6gLPYAxhcK1sYNqg1wYHBLf5NhF4A=="
            self.org = "Slim"
            self.bucket = "Smart Hospital Bed"
            client = InfluxDBClient(url="http://localhost:8086", token=token)

            self.write_api = client.write_api(write_options=SYNCHRONOUS)

            point = Point(measurement).field(fieldKey, fieldValue).time(
                datetime.utcnow(), WritePrecision.S)
            self.write_api.write(self.bucket, self.org, point)
        except:
            pass


if (__name__ == '__main__'):
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
