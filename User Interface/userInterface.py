import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *  
import os
import cv2
from PIL import ImageTk, Image
import serial
import json
import numpy as np
import simpleaudio as sa


try:
    serialWeight = serial.Serial('COM4')
    weightDisconnected = False
except:
    weightDisconnected = True

try:
    serialTemp = serial.Serial('COM3')
    tempDisconnected = False
except:
    tempDisconnected = True

try:
    serialUrineBag = serial.Serial('COM7')
    urineDisconnected = False
except:
    urineDisconnected = True

firstInit = True


class smartBedUI:

    def __init__(self, master = None):
        global firstInit

        self.master = master
        self.frame_1 = ttk.Frame(self.master)
        self.windowWidth = self.master.winfo_width()
        self.windowHeight = self.master.winfo_height()
        self.cellSize = self.windowHeight / 10.75

        if (firstInit):
            self.uiPath = os.path.realpath(__file__).replace('userInterface.py', '')

        self.bg = tk.Canvas(self.frame_1)
        self.bg.config(bg = '#000000')
        self.bg.place(anchor = 'nw', height = str(self.windowHeight), width = str(self.windowWidth), x = '0', y = '0')
        self.bgImg = ImageTk.PhotoImage(Image.open(self.uiPath + 'alert.png').resize((1, 1)))
        self.bgOnCanvas = self.bg.create_image(0, 0, anchor = NW, image = self.bgImg)
        self.bg.create_text(int(self.cellSize*2.5), int(self.cellSize*1.125), fill = '#ffffff', font = (None, int(self.cellSize*0.35)), text = 'Weight Distribution')
        self.bg.create_text(int(self.cellSize*7.25), int(self.cellSize*1.125), fill = '#ffffff', font = (None, int(self.cellSize*0.35)), text = 'Heat Map')
        self.bg.create_text(int(self.cellSize*11.125), int(self.cellSize*1.125), fill = '#ffffff', font = (None, int(self.cellSize*0.35)), text = 'Pulse')
        self.frame_1_1 = ttk.Frame(self.frame_1)

        self.contour = []
        y = 0
        index = 0
        for i in range (6):
            x = 0

            for j in range (4):
                self.contour.append(tk.Canvas(self.frame_1_1))
                self.contour[index].config(bg = '#000000')
                self.contour[index].place(anchor = 'nw', height = str(self.cellSize*1.375), width = str(self.cellSize*1.375), x = str(x), y = str(y))
                index += 1
                x += self.cellSize*1.375

            y += self.cellSize*1.375
        
        self.frame_1_1.place(anchor = 'nw', height = str(self.cellSize*8.25), width = str(self.cellSize*5.5), x = str(self.cellSize*0.5), y = str(self.cellSize*1.5))
        self.frame_1_2_3_4_5_6_7 = ttk.Frame(self.frame_1)
        self.heatMap = tk.Canvas(self.frame_1_2_3_4_5_6_7)
        self.heatMap.config(bg = '#000000')
        self.heatMap.place(anchor = 'nw', height = str(self.cellSize*5.25), width = str(self.cellSize*4), x = '0', y = '0')
        self.heatMapImg = ImageTk.PhotoImage(Image.open(self.uiPath + 'alert.png').resize((1, 1)))
        self.mapOnCanvas = self.heatMap.create_image(0, 0, anchor = NW, image = self.heatMapImg)
        self.frame_1_2_3_4_5_6_7.place(anchor = 'nw', height = str(self.cellSize*5.25), width = str(self.cellSize*4), x = str(self.cellSize*6.25), y = str(self.cellSize*1.5))
        self.frame_1_2 = ttk.Frame(self.frame_1)
        self.canvas_1_1 = tk.Canvas(self.frame_1_2)
        self.canvas_1_1.config(bg = '#000000')
        self.canvas_1_1.place(anchor = 'nw', height = str(self.cellSize*2.75), width = str(self.cellSize*8.25), x = '0', y = '0')
        self.frame_1_2.place(anchor = 'nw', height = str(self.cellSize*2.75), width = str(self.cellSize*8.25), x = str(self.cellSize*10.5), y = str(self.cellSize*1.5))
        self.frame_1_2_3 = ttk.Frame(self.frame_1)
        self.canvas_2_1 = tk.Canvas(self.frame_1_2_3)
        self.canvas_2_1.config(bg = '#000000')
        self.canvas_2_1.place(anchor = 'nw', height = str(self.cellSize*2.25), width = str(self.cellSize*2.25), x = '0', y = '0')
        self.message_1 = tk.Label(self.frame_1_2_3, font = (None, int(self.cellSize*0.275)))
        self.message_1.config(bg = '#000000', foreground = '#00ff80', text = 'BPM')
        self.message_1.place(anchor = 'nw', height = str(self.cellSize*0.575), width = str(self.cellSize*1.125), x = str(self.cellSize*1.125), y = str(self.cellSize*1.625))
        self.heartrate = tk.Label(self.frame_1_2_3, font = (None, int(self.cellSize*0.8875)))
        self.heartrate.config(bg = '#000000', foreground = '#00ff80', text = '--')
        self.heartrate.place(anchor = 'nw', height = str(self.cellSize), width = str(self.cellSize*2.25), x = '0', y = str(self.cellSize*0.675))
        self.img2 = ImageTk.PhotoImage(Image.open(self.uiPath + 'pulse.png').resize((int(self.cellSize*0.575)+1, int(self.cellSize*0.575)+1), Image.ANTIALIAS))      
        self.canvas_2_1.create_image(self.cellSize*0.1, self.cellSize*0.1, anchor = NW, image = self.img2) 
        self.canvas_2_1.image = self.img2
        self.frame_1_2_3.place(anchor = 'nw', height = str(self.cellSize*2.25), width = str(self.cellSize*2.25), x = str(self.cellSize*10.5), y = str(self.cellSize*4.5))
        self.frame_1_2_3_4 = ttk.Frame(self.frame_1)
        self.canvas_2_3 = tk.Canvas(self.frame_1_2_3_4)
        self.canvas_2_3.config(bg = '#000000')
        self.canvas_2_3.place(anchor = 'nw', height = str(self.cellSize*2.25), width = str(self.cellSize*2.25), x = '0', y = '0')
        self.message_1_3 = tk.Label(self.frame_1_2_3_4, font = (None, int(self.cellSize*0.275)))
        self.message_1_3.config(bg = '#000000', foreground = '#ff0000', text = 'F')
        self.message_1_3.place(anchor = 'nw', height = str(self.cellSize*0.575), width = str(self.cellSize*0.575), x = str(self.cellSize*1.625), y = str(self.cellSize*1.625))
        self.temperature = tk.Label(self.frame_1_2_3_4, font = (None, int(self.cellSize*0.8875)))
        self.temperature.config(bg = '#000000', foreground = '#ff0000', text = '--')
        self.temperature.place(anchor = 'nw', height = str(self.cellSize), width = str(self.cellSize*2.25), x = '0', y = str(self.cellSize*0.675))
        self.img3 = ImageTk.PhotoImage(Image.open(self.uiPath + 'temp.png').resize((int(self.cellSize*0.2875)+1, int(self.cellSize*0.575)+1), Image.ANTIALIAS))      
        self.canvas_2_3.create_image(self.cellSize*0.1, self.cellSize*0.1, anchor = NW, image = self.img3) 
        self.canvas_2_3.image = self.img3
        self.frame_1_2_3_4.place(anchor = 'nw', height = str(self.cellSize*2.25), width = str(self.cellSize*2.25), x = str(self.cellSize*13), y = str(self.cellSize*4.5))
        self.frame_1_2_3_4_5 = ttk.Frame(self.frame_1)
        self.canvas_2_4 = tk.Canvas(self.frame_1_2_3_4_5)
        self.canvas_2_4.config(bg = '#000000')
        self.canvas_2_4.place(anchor = 'nw', height = str(self.cellSize*2.25), width = str(self.cellSize*3.25), x = '0', y = '0')
        self.message_1_4 = tk.Label(self.frame_1_2_3_4_5, font = (None, int(self.cellSize*0.275)))
        self.message_1_4.config(bg = '#000000', foreground = '#ff8040', text = 'KG')
        self.message_1_4.place(anchor = 'nw', height = str(self.cellSize*0.575), width = str(self.cellSize*0.575), x = str(self.cellSize*2.625), y = str(self.cellSize*1.625))
        self.weight = tk.Label(self.frame_1_2_3_4_5, font = (None, int(self.cellSize*0.45)))
        self.weight.config(bg = '#000000', foreground = '#ff8040', text = '-- to --')
        self.weight.place(anchor = 'nw', height = str(self.cellSize), width = str(self.cellSize*3.25), x = '0', y = str(self.cellSize*0.675))
        self.img4 = ImageTk.PhotoImage(Image.open(self.uiPath + 'weight.png').resize((int(self.cellSize*0.575)+1, int(self.cellSize*0.575)+1), Image.ANTIALIAS))      
        self.canvas_2_4.create_image(self.cellSize*0.1, self.cellSize*0.1, anchor = NW, image = self.img4) 
        self.canvas_2_4.image = self.img4
        self.frame_1_2_3_4_5.place(anchor = 'nw', height = str(self.cellSize*2.25), width = str(self.cellSize*3.25), x = str(self.cellSize*15.5), y = str(self.cellSize*4.5))
        self.frame_1_2_3_4_5_6 = ttk.Frame(self.frame_1)
        self.canvas_2_5 = tk.Canvas(self.frame_1_2_3_4_5_6)
        self.canvas_2_5.config(bg = '#000000')
        self.canvas_2_5.place(anchor = 'nw', height = str(self.cellSize*2.75), width = str(self.cellSize*2.25), x = '0', y = '0')
        self.message_1_5 = tk.Label(self.frame_1_2_3_4_5_6, font = (None, int(self.cellSize*0.275)))
        self.message_1_5.config(bg = '#000000', foreground = '#ffff00', text = '%')
        self.message_1_5.place(anchor = 'nw', height = str(self.cellSize*0.575), width = str(self.cellSize*0.575), x = str(self.cellSize*1.625), y = str(self.cellSize*2))
        self.urinebag = tk.Label(self.frame_1_2_3_4_5_6, font = (None, int(self.cellSize*0.8875)))
        self.urinebag.config(bg = '#000000', foreground = '#ffff00', text = '--')
        self.urinebag.place(anchor = 'nw', height = str(self.cellSize), width = str(self.cellSize*2.25), x = '0', y = str(self.cellSize*0.875))
        self.img5 = ImageTk.PhotoImage(Image.open(self.uiPath + 'urineBag.png').resize((int(self.cellSize*0.2875)+1, int(self.cellSize*0.575)+1), Image.ANTIALIAS))      
        self.canvas_2_5.create_image(self.cellSize*0.1, self.cellSize*0.1, anchor = NW, image = self.img5) 
        self.canvas_2_5.image = self.img5
        self.frame_1_2_3_4_5_6.place(anchor = 'nw', height = str(self.cellSize*2.75), width = str(self.cellSize*2.25), x = str(self.cellSize*16.5), y = str(self.cellSize*7))
        self.frame_1_2_7 = ttk.Frame(self.frame_1)
        self.canvas_6_1 = tk.Canvas(self.frame_1_2_7)
        self.canvas_6_1.config(bg = '#000000')
        self.canvas_6_1.place(anchor = 'nw', height = str(self.cellSize*2.75), width = str(self.cellSize*10), x = '0', y = '0')
        self.alert = tk.Label(self.frame_1_2_7, font = (None, int(self.cellSize*0.35)))
        self.alert.config(bg = '#000000', foreground = '#ffffff', text = 'Unoccupied')
        self.alert.place(anchor = 'nw', height = str(self.cellSize*2.625), width = str(self.cellSize*9.125), x = str(self.cellSize*0.725), y = str(self.cellSize*0.0475))
        self.img6 = ImageTk.PhotoImage(Image.open(self.uiPath + 'alert.png').resize((int(self.cellSize*0.575)+1, int(self.cellSize*0.575)+1), Image.ANTIALIAS))
        self.canvas_6_1.create_image(self.cellSize*0.1, self.cellSize*0.1, anchor = NW, image = self.img6) 
        self.canvas_6_1.image = self.img6
        self.frame_1_2_7.place(anchor = 'nw', height = str(self.cellSize*2.75), width = str(self.cellSize*10), x = str(self.cellSize*6.25), y = str(self.cellSize*7))
        self.frame_1.place(anchor = 'nw', height = str(self.windowHeight), width = str(self.windowWidth), x = '0', y = '0')

        self.mainwindow = self.frame_1

        if (firstInit):
            firstInit = False

            self.startup = sa.WaveObject.from_wave_file(self.uiPath + 'Startup.wav')
            self.startup.play()

            self.master.geometry('{0}x{1}+0+0'.format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
            self.master.bind('<Configure>', self.onResize)

            self.bgVid = 'bgMain.mp4'
            self.cap = cv2.VideoCapture(self.uiPath + self.bgVid)
            self.isOccupied = False
            self.firstTemp = True
            self.alertText = ['', '', '']
            self.previousAlert = ['', '', '']
            self.occupiedTone = sa.WaveObject.from_wave_file(self.uiPath + 'occupied.wav')
            self.unoccupiedTone = sa.WaveObject.from_wave_file(self.uiPath + 'unoccupied.wav')
            self.alertTone = sa.WaveObject.from_wave_file(self.uiPath + 'alert.wav')

            self.update()
            self.updateWeight()
            self.updateTemp()
            self.updateUrineBag()


    def run(self):
        self.mainwindow.mainloop()


    def onResize(self, event):
        previousWidth = self.windowWidth
        previousHeight = self.windowHeight

        if (previousWidth != self.master.winfo_width() or previousHeight != self.master.winfo_height()):
            self.__init__(self.master)


    def update(self):
        global playAlert

        try:
            if (self.bgVid == 'bgMain.mp4' and playAlert.is_playing()):
                self.bgVid == 'bgWarn.mp4'
                self.cap = cv2.VideoCapture(self.uiPath + self.bgVid)
            elif (self.bgVid == 'bgWarn.mp4' and not (playAlert.is_playing())):
                self.bgVid == 'bgMain.mp4'
                self.cap = cv2.VideoCapture(self.uiPath + self.bgVid)
        except:
            pass
        
        try:
            _, frame = self.cap.read()
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            self.bgImg = ImageTk.PhotoImage(Image.fromarray(cv2image).resize((self.windowWidth, self.windowHeight), Image.ANTIALIAS))
            self.bg.itemconfig(self.bgOnCanvas, image = self.bgImg)
        except:
            self.cap = cv2.VideoCapture(self.uiPath + self.bgVid)

        combinedAlert = self.alertText[0] + self.alertText[1] + self.alertText[2]
        combinedAlert = combinedAlert.rstrip('\n')
        self.alert.config(text = combinedAlert)

        self.mainwindow.after(42, self.update)
        
        
    def updateWeight(self):
        global serialWeight
        global weightDisconnected
        global playAlert
        self.alertText[0] = ''

        if (weightDisconnected):
            self.alertText[0] += 'Weight module disconnected!' + '\n'
        else:
            weightJSON = serialWeight.readline().decode().strip()

            while (not weightJSON.startswith('{')):
                print('Weight Port:', weightJSON)
                weightJSON = serialWeight.readline().decode().strip()

            print('Weight Port:', weightJSON)
            weightDict = json.loads(weightJSON)
            wt = weightDict['weight']

            if (wt == 0.00):
                self.isOccupied = False
                wt = '-- to --'
                self.weight.config(text = wt)
                self.alertText[0] += 'Unoccupied' + '\n'
                if (not('Unoccupied' in self.previousAlert[0])):
                    try:
                        if (not playUnoccupied.is_playing()):
                            playUnoccupied = self.unoccupiedTone.play()
                    except:
                        playUnoccupied = self.unoccupiedTone.play()
            else:
                self.isOccupied = True
                wt = str(round(wt)-5) + ' to ' + str(round(wt)+5)
                self.weight.config(text = wt)
                self.alertText[0] += 'Patient on bed' + '\n'
                if (not('Patient on bed' in self.previousAlert[0])):
                    try:
                        if (not playOccupied.is_playing()):
                            playOccupied = self.occupiedTone.play()
                    except:
                        playOccupied = self.occupiedTone.play()
            
            diffs = weightDict['diff']
            for i in range (24):
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
                self.contour[i].config(bg = color)

            if (self.isOccupied):
                weightAlert = weightDict['msg']

                if (weightAlert != ''):
                    self.alertText[0] += 'Patient hasn\'t been repositioned! Please do it.' + '\n'

                    try:
                        if (not playAlert.is_playing()):
                            playAlert = self.alertTone.play()
                    except:
                        playAlert = self.alertTone.play()

            self.previousAlert[0] = self.alertText[0]

            serialWeight.flush()
            serialWeight.flushInput()
            serialWeight.flushOutput()

        self.mainwindow.after(42, self.updateWeight)


    def updateTemp(self):
        global serialTemp
        global tempDisconnected
        global playAlert
        self.alertText[1] = ''

        if (tempDisconnected):
            self.alertText[1] += 'Temperature module disconnected!' + '\n'
        else:
            if (self.firstTemp):
                self.firstTemp = False
                bedMat = np.zeros((80, 36, 3))
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
                bedMat[np.where(np.logical_and(np.logical_and(c1Mask == True, c2Mask == True), c3Mask == True))] = 123

            if (not self.isOccupied):
                tempValue = serialTemp.readline().decode().strip()
                print('Temperature Port:', tempValue)
                msg = np.array(tempValue.split(','), dtype = float)

                for i in range(80):
                    for j in range(36):

                        if (bedMat[i][j][0] == 1.0):
                            bedMat[i][j][0] = msg[0]        
                        elif (bedMat[i][j][0] == 2.0):
                            bedMat[i][j][0] = msg[1]
                        elif (bedMat[i][j][0] == 3.0):
                            bedMat[i][j][0] = msg[2]
                        elif (bedMat[i][j][0] == 12.0):
                            bedMat[i][j][0] = (msg[0] + msg[1]) / 2
                        elif (bedMat[i][j][0] == 13.0):
                            bedMat[i][j][0] = (msg[0] + msg[2]) / 2
                        elif (bedMat[i][j][0] == 23.0):
                            bedMat[i][j][0] = (msg[1] + msg[2]) / 2
                        elif (bedMat[i][j][0] == 123.0):
                            bedMat[i][j][0] = (msg[0] + msg[1] + msg[2]) / 3

                heatMapArray = int(bedMat * 6)
                self.heatMapImg = ImageTk.PhotoImage(Image.fromarray(heatMapArray, 'RGB').resize((int(self.cellSize*5.25), int(self.cellSize*4)), Image.ANTIALIAS))
                self.heatMap.itemconfig(self.mapOnCanvas, image = self.heatMapImg)

            self.previousAlert[1] = self.alertText[1]

            serialTemp.flush()
            serialTemp.flushInput()
            serialTemp.flushOutput()

        self.mainwindow.after(42, self.updateTemp)


    def updateUrineBag(self):
        global serialUrineBag
        global urineDisconnected
        global playAlert
        self.alertText[2] = ''

        if (urineDisconnected):
            self.alertText[2] += 'Urine bag module disconnected!' + '\n'
        else:
            try:
                urineBagValue = serialUrineBag.readline().decode().strip()
                print('Urine Bag Port:', urineBagValue)

                if (not self.isOccupied):
                    self.urinebag.config(text = '--')
                else:

                    if (urineBagValue == '-1'):
                        self.urinebag.config(text = '--')
                        self.alertText[2] += 'Urine Bag removed! Please attach one.' + '\n'

                        if (not('Urine Bag removed! Please attach one.' in self.previousAlert[2])):
                            try:
                                if (not playAlert.is_playing()):
                                    playAlert = self.alertTone.play()
                            except:
                                playAlert = self.alertTone.play()

                    elif (urineBagValue == 'PP'):
                        self.alertText[2] += 'Patient hasn\'t urinated in last 6 hours!' + '\n'

                        try:
                            if (not playAlert.is_playing()):
                                playAlert = self.alertTone.play()
                        except:
                            playAlert = self.alertTone.play()

                    elif (urineBagValue.isnumeric()):
                        self.urinebag.config(text = urineBagValue)
                        urineBagValue = int(float(urineBagValue))

                        if (urineBagValue == 100):
                            self.alertText[2] += 'Urine Bag full! Please change it ASAP.' + '\n'

                            try:
                                if (not playAlert.is_playing()):
                                    playAlert = self.alertTone.play()
                            except:
                                playAlert = self.alertTone.play()

                        elif (urineBagValue > 80):
                            self.alertText[2] += 'Urine Bag almost full! Please drain / change it.' + '\n'

                            try:
                                if (not playAlert.is_playing()):
                                    playAlert = self.alertTone.play()
                            except:
                                playAlert = self.alertTone.play()

            except:
                print('Urine Bag Port: Garbage')

            self.previousAlert[2] = self.alertText[2]

            serialUrineBag.flush()
            serialUrineBag.flushInput()
            serialUrineBag.flushOutput()

        self.mainwindow.after(42, self.updateUrineBag)


if __name__ == '__main__':
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    app = smartBedUI(root)
    app.run()
