import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *  
from PIL import ImageTk, Image
import os
import serial
import json
import simpleaudio as sa


uiPath = os.path.realpath(__file__).replace('userInterface.py', '')
weightDisconnected = False
tempDisconnected = False
urineDisconnected = False
firstInit = True
previousAlert = ''

class UserinterfaceApp:

    def __init__(self, master=None):
        global firstInit

        self.master = master
        self.frame_1 = ttk.Frame(self.master)
        self.windowWidth = self.master.winfo_width()
        self.windowHeight = self.master.winfo_height()
        self.cellSize = self.windowHeight / 10

        self.canvas_1_1_1 = tk.Canvas(self.frame_1)
        self.canvas_1_1_1.config(background='#000000', height=str(self.windowHeight), width=str(self.windowWidth))
        self.canvas_1_1_1.place(anchor='nw', height=str(self.windowHeight), width=str(self.windowWidth), x='0', y='0')
        self.img = ImageTk.PhotoImage(Image.open(uiPath + 'Background.jpg').resize((self.windowWidth, self.windowHeight), Image.ANTIALIAS))  
        self.canvas_1_1_1.create_image(0, 0, anchor=NW, image=self.img) 
        self.canvas_1_1_1.image = self.img  
        self.frame_1_1 = ttk.Frame(self.frame_1)

        self.contour = []
        y = 0
        index = 0
        for i in range (6):
            x = 0
            for j in range (4):
                self.contour.append(tk.Canvas(self.frame_1_1))
                self.contour[index].config(background='#000000')
                self.contour[index].place(anchor='nw', height=str(self.cellSize*1.375), width=str(self.cellSize*1.375), x=str(x), y=str(y))
                index += 1
                x += self.cellSize*1.375
            y += self.cellSize*1.375
        
        self.frame_1_1.place(anchor='nw', height=str(self.cellSize*8.25), width=str(self.cellSize*5.5), x=str(self.cellSize), y=str(self.cellSize))
        self.frame_1_2 = ttk.Frame(self.frame_1)
        self.canvas_1_1 = tk.Canvas(self.frame_1_2)
        self.canvas_1_1.config(background='#000000')
        self.canvas_1_1.place(anchor='nw', height=str(self.cellSize*2.75), width=str(self.cellSize*10), x='0', y='0')
        self.frame_1_2.place(anchor='nw', height=str(self.cellSize*2.75), width=str(self.cellSize*10), x=str(self.cellSize*7.25), y=str(self.cellSize))
        self.frame_1_2_3 = ttk.Frame(self.frame_1)
        self.canvas_2_1 = tk.Canvas(self.frame_1_2_3)
        self.canvas_2_1.config(background='#000000')
        self.canvas_2_1.place(anchor='nw', height=str(self.cellSize*2.25), width=str(self.cellSize*2.25), x='0', y='0')
        self.message_1 = tk.Label(self.frame_1_2_3, font=(None, int(self.cellSize/3.75)))
        self.message_1.config(background='#000000', foreground='#00ff80', text='BPM')
        self.message_1.place(anchor='nw', height=str(self.cellSize/1.75), width=str(self.cellSize*1.125), x=str(self.cellSize*1.125), y=str(self.cellSize*1.625))
        self.heartrate = tk.Label(self.frame_1_2_3, font=(None, int(self.cellSize/1.125)))
        self.heartrate.config(background='#000000', foreground='#00ff80', text='--')
        self.heartrate.place(anchor='nw', height=str(self.cellSize), width=str(self.cellSize*2.25), x='0', y=str(self.cellSize/1.5))
        self.img2 = ImageTk.PhotoImage(Image.open(uiPath + 'Heart Rate.png').resize((int(self.cellSize/1.75)+1, int(self.cellSize/1.75)+1), Image.ANTIALIAS))      
        self.canvas_2_1.create_image(self.cellSize/10, self.cellSize/10, anchor=NW, image=self.img2) 
        self.canvas_2_1.image = self.img2
        self.frame_1_2_3.place(anchor='nw', height=str(self.cellSize*2.25), width=str(self.cellSize*2.25), x=str(self.cellSize*7.25), y=str(self.cellSize*4))
        self.frame_1_2_3_4 = ttk.Frame(self.frame_1)
        self.canvas_2_3 = tk.Canvas(self.frame_1_2_3_4)
        self.canvas_2_3.config(background='#000000')
        self.canvas_2_3.place(anchor='nw', height=str(self.cellSize*2.25), width=str(self.cellSize*2.25), x='0', y='0')
        self.message_1_3 = tk.Label(self.frame_1_2_3_4, font=(None, int(self.cellSize/3.75)))
        self.message_1_3.config(background='#000000', foreground='#ff0000', text='F')
        self.message_1_3.place(anchor='nw', height=str(self.cellSize/1.75), width=str(self.cellSize/1.75), x=str(self.cellSize*1.625), y=str(self.cellSize*1.625))
        self.temperature = tk.Label(self.frame_1_2_3_4, font=(None, int(self.cellSize/1.125)))
        self.temperature.config(background='#000000', foreground='#ff0000', text='--')
        self.temperature.place(anchor='nw', height=str(self.cellSize), width=str(self.cellSize*2.25), x='0', y=str(self.cellSize/1.5))
        self.img3 = ImageTk.PhotoImage(Image.open(uiPath + 'Temperature.png').resize((int(self.cellSize/1.75)+1, int(self.cellSize/1.75)+1), Image.ANTIALIAS))      
        self.canvas_2_3.create_image(self.cellSize/10, self.cellSize/10, anchor=NW, image=self.img3) 
        self.canvas_2_3.image = self.img3
        self.frame_1_2_3_4.place(anchor='nw', height=str(self.cellSize*2.25), width=str(self.cellSize*2.25), x=str(self.cellSize*9.5), y=str(self.cellSize*4))
        self.frame_1_2_3_4_5 = ttk.Frame(self.frame_1)
        self.canvas_2_4 = tk.Canvas(self.frame_1_2_3_4_5)
        self.canvas_2_4.config(background='#000000')
        self.canvas_2_4.place(anchor='nw', height=str(self.cellSize*2.25), width=str(self.cellSize*3.25), x='0', y='0')
        self.message_1_4 = tk.Label(self.frame_1_2_3_4_5, font=(None, int(self.cellSize/3.75)))
        self.message_1_4.config(background='#000000', foreground='#ff8040', text='KG')
        self.message_1_4.place(anchor='nw', height=str(self.cellSize/1.75), width=str(self.cellSize/1.75), x=str(self.cellSize*2.625), y=str(self.cellSize*1.625))
        self.weight = tk.Label(self.frame_1_2_3_4_5, font=(None, int(self.cellSize/2.25)))
        self.weight.config(background='#000000', foreground='#ff8040', text='-- to --')
        self.weight.place(anchor='nw', height=str(self.cellSize), width=str(self.cellSize*3.25), x='0', y=str(self.cellSize/1.5))
        self.img4 = ImageTk.PhotoImage(Image.open(uiPath + 'Weight.png').resize((int(self.cellSize/1.75)+1, int(self.cellSize/1.75)+1), Image.ANTIALIAS))      
        self.canvas_2_4.create_image(self.cellSize/10, self.cellSize/10, anchor=NW, image=self.img4) 
        self.canvas_2_4.image = self.img4
        self.frame_1_2_3_4_5.place(anchor='nw', height=str(self.cellSize*2.25), width=str(self.cellSize*3.25), x=str(self.cellSize*14), y=str(self.cellSize*4))
        self.frame_1_2_3_4_5_6 = ttk.Frame(self.frame_1)
        self.canvas_2_5 = tk.Canvas(self.frame_1_2_3_4_5_6)
        self.canvas_2_5.config(background='#000000')
        self.canvas_2_5.place(anchor='nw', height=str(self.cellSize*2.25), width=str(self.cellSize*2.25), x='0', y='0')
        self.message_1_5 = tk.Label(self.frame_1_2_3_4_5_6, font=(None, int(self.cellSize/3.75)))
        self.message_1_5.config(background='#000000', foreground='#ffff00', text='%')
        self.message_1_5.place(anchor='nw', height=str(self.cellSize/1.75), width=str(self.cellSize/1.75), x=str(self.cellSize*1.625), y=str(self.cellSize*1.625))
        self.urinebag = tk.Label(self.frame_1_2_3_4_5_6, font=(None, int(self.cellSize/1.125)))
        self.urinebag.config(background='#000000', foreground='#ffff00', text='--')
        self.urinebag.place(anchor='nw', height=str(self.cellSize), width=str(self.cellSize*2.25), x='0', y=str(self.cellSize/1.5))
        self.img5 = ImageTk.PhotoImage(Image.open(uiPath + 'Urine Bag.png').resize((int(self.cellSize/1.75)+1, int(self.cellSize/1.75)+1), Image.ANTIALIAS))      
        self.canvas_2_5.create_image(self.cellSize/10, self.cellSize/10, anchor=NW, image=self.img5) 
        self.canvas_2_5.image = self.img5
        self.frame_1_2_3_4_5_6.place(anchor='nw', height=str(self.cellSize*2.25), width=str(self.cellSize*2.25), x=str(self.cellSize*11.75), y=str(self.cellSize*4))
        self.frame_1_2_7 = ttk.Frame(self.frame_1)
        self.canvas_6_1 = tk.Canvas(self.frame_1_2_7)
        self.canvas_6_1.config(background='#000000')
        self.canvas_6_1.place(anchor='nw', height=str(self.cellSize*2.75), width=str(self.cellSize*10), x='0', y='0')
        self.alert = tk.Label(self.frame_1_2_7, font=(None, int(self.cellSize/2.875)))
        self.alert.config(background='#000000', foreground='#ffffff', text='Unoccupied')
        self.alert.place(anchor='nw', height=str(self.cellSize*2.625), width=str(self.cellSize*9.125), x=str(self.cellSize/1.375), y=str(self.cellSize/22.125))
        self.img6 = ImageTk.PhotoImage(Image.open(uiPath + 'Alert.png').resize((int(self.cellSize/1.75)+1, int(self.cellSize/1.75)+1), Image.ANTIALIAS))      
        self.canvas_6_1.create_image(self.cellSize/10, self.cellSize/10, anchor=NW, image=self.img6) 
        self.canvas_6_1.image = self.img6
        self.frame_1_2_7.place(anchor='nw', height=str(self.cellSize*2.75), width=str(self.cellSize*10), x=str(self.cellSize*7.25), y=str(self.cellSize*6.5))
        self.frame_1.place(anchor='nw', height=str(self.windowHeight), width=str(self.windowWidth), x='0', y='0')

        self.mainwindow = self.frame_1

        if (firstInit):
            firstInit = False
            self.master.geometry('{0}x{1}+0+0'.format(self.master.winfo_screenwidth(), self.master.winfo_screenheight()))
            self.master.bind('<Configure>', self.on_resize)
            startup = sa.WaveObject.from_wave_file(uiPath + 'Startup.wav')
            startup.play()
            self.update()


    def run(self):
        self.mainwindow.mainloop()
        
        
    def update(self):
        global urineBagValue
        global previousAlert
        alertText = ''
        unoccupied = sa.WaveObject.from_wave_file(uiPath + 'Unoccupied.wav')
        occupied = sa.WaveObject.from_wave_file(uiPath + 'Occupied.wav')
        alert = sa.WaveObject.from_wave_file(uiPath + 'Alert.wav')

        if (weightDisconnected):
            alertText += 'Contour & weight estimator disconnected!' + '\n'
        else:
            weightJSON = serialWeight.readline().decode().strip()
            while (not weightJSON.startswith('{')):
                print('Weight Port:', weightJSON)
                weightJSON = serialWeight.readline().decode().strip()
            print('Weight Port:', weightJSON)
            weightDict = json.loads(weightJSON)
            wt = weightDict['weight']
            if (wt == 0.00):
                isOccupied = False
                wt = '-- to --'
                self.weight.config(text=wt)
                alertText += 'Unoccupied' + '\n'
                if (not('Unoccupied' in previousAlert)):
                    try:
                        if(not playUnoccupied.is_playing()):
                            playUnoccupied = unoccupied.play()
                    except:
                        playUnoccupied = unoccupied.play()
            else:
                isOccupied = True
                wt = str(round(wt)-5) + ' to ' + str(round(wt)+5)
                self.weight.config(text=wt)
                alertText += 'Patient on bed' + '\n'
                if (not('Patient on bed' in previousAlert)):
                    try:
                        if(not playOccupied.is_playing()):
                            playOccupied = occupied.play()
                    except:
                        playOccupied = occupied.play()
            
            diffs = weightDict['diff']
            for i in range (24):
                diff = int(float(diffs[i])) * 2
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
                self.contour[i].config(background=color)

            if (isOccupied):
                weightAlert = weightDict['msg']
                if (weightAlert != ''):
                    alertText += 'Patient hasn\'t been repositioned! Please do it.' + '\n'
                    try:
                        if(not playAlert.is_playing()):
                            playAlert = alert.play()
                    except:
                        playAlert = alert.play()

        if (tempDisconnected):
            alertText += 'Temperature predictor disconnected!' + '\n'
        else:
            tempValue = serialTemp.readline().decode().strip()
            print('Temperature Port:', tempValue)
            if (not isOccupied or tempValue == '--' or tempValue == '-' or tempValue == ''):
                tp = '--'
                self.temperature.config(text=tp)
            elif (tempValue != 'nan' and tempValue != 'an' and tempValue != 'n'):
                    tp = str(int(float(tempValue)))
                    self.temperature.config(text=tp)

        if (urineDisconnected):
            alertText += 'Urine bag module disconnected!' + '\n'
        else:
            try:
                urineBagValue = serialUrineBag.readline().decode().strip()
                print('Urine Bag Port:', urineBagValue)
                if (not isOccupied or urineBagValue == '-1'):
                    self.urinebag.config(text='--')
                elif (urineBagValue == 'PP'):
                    alertText += 'Patient hasn\'t urinated in last 6 hours!' + '\n'
                    try:
                        if(not playAlert.is_playing()):
                            playAlert = alert.play()
                    except:
                        playAlert = alert.play()
                elif (urineBagValue.isnumeric()):
                    self.urinebag.config(text=urineBagValue)
                    urineBagValue = int(float(urineBagValue))
                    if (urineBagValue == 100):
                        alertText += 'Urine Bag full! Please change it ASAP.' + '\n'
                        try:
                            if(not playAlert.is_playing()):
                                playAlert = alert.play()
                        except:
                            playAlert = alert.play()
                    elif (urineBagValue > 75):
                        alertText += 'Urine Bag almost full! Please drain / change it.' + '\n'
                        try:
                            if(not playAlert.is_playing()):
                                playAlert = alert.play()
                        except:
                            playAlert = alert.play()
            except:
                print('Urine Bag Port: Garbage')

        self.alert.config(text = alertText)
        previousAlert = alertText

        if (not weightDisconnected):
            serialWeight.flush()
            serialWeight.flushInput()
            serialWeight.flushOutput()

        if (not tempDisconnected):
            serialTemp.flush()
            serialTemp.flushInput()
            serialTemp.flushOutput()

        if (not urineDisconnected):
            serialUrineBag.flush()
            serialUrineBag.flushInput()
            serialUrineBag.flushOutput()

        self.mainwindow.after(42, self.update)


    def on_resize(self, event):
        previousWidth = self.windowWidth
        previousHeight = self.windowHeight
        if (previousWidth != self.master.winfo_width() or previousHeight != self.master.winfo_height()):
            self.__init__(self.master)


if __name__ == '__main__':
    try:
        serialWeight = serial.Serial('COM4')
    except:
        weightDisconnected = True
    
    try:
        serialTemp = serial.Serial('COM6')
    except:
        tempDisconnected = True
    
    try:
        serialUrineBag = serial.Serial('COM7')
    except:
        urineDisconnected = True
    
    root = tk.Tk()
    app = UserinterfaceApp(root)
    app.run()
