import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *  
from PIL import ImageTk, Image
import serial
import numpy as np
import random


testing = True


class UserinterfaceApp:
    def __init__(self, master=None):
        self.count = 0
        self.frame_1 = ttk.Frame(master)
        self.canvas_1_1_1 = tk.Canvas(self.frame_1)
        self.canvas_1_1_1.config(background='#000000', confine='true', height='768')
        self.canvas_1_1_1.config(width='1366')
        self.canvas_1_1_1.place(anchor='nw', height='768', width='1366', x='0', y='0')
        self.canvas_1_1_1.pack()      
        self.img = ImageTk.PhotoImage(Image.open("Background.jpg"))      
        self.canvas_1_1_1.create_image(0,0, anchor=NW, image=self.img) 
        self.canvas_1_1_1.image = self.img  
        self.frame_1_1 = ttk.Frame(self.frame_1)
        self.canvas_1 = tk.Canvas(self.frame_1_1)
        self.canvas_1.config(background='#000000', confine='true', height='150', relief='flat')
        self.canvas_1.config(width='150')
        self.canvas_1.place(anchor='nw', height='150', width='150', x='0', y='0')
        self.canvas_2 = tk.Canvas(self.frame_1_1)
        self.canvas_2.config(background='#000000', height='150', width='150')
        self.canvas_2.place(anchor='nw', height='150', width='150', x='150', y='0')
        self.canvas_3 = tk.Canvas(self.frame_1_1)
        self.canvas_3.config(background='#000000', height='150', width='150')
        self.canvas_3.place(anchor='nw', height='150', width='150', x='300', y='0')
        self.canvas_4 = tk.Canvas(self.frame_1_1)
        self.canvas_4.config(background='#000000', height='150', width='150')
        self.canvas_4.place(anchor='nw', height='150', width='150', x='150', y='150')
        self.canvas_5 = tk.Canvas(self.frame_1_1)
        self.canvas_5.config(background='#000000', height='150', relief='flat', width='150')
        self.canvas_5.place(anchor='nw', height='150', width='150', x='300', y='150')
        self.canvas_6 = tk.Canvas(self.frame_1_1)
        self.canvas_6.config(background='#000000', height='150', relief='flat', width='150')
        self.canvas_6.place(anchor='nw', height='150', width='150', x='0', y='300')
        self.canvas_7 = tk.Canvas(self.frame_1_1)
        self.canvas_7.config(background='#000000', height='150', takefocus=False, width='150')
        self.canvas_7.place(anchor='nw', height='150', width='150', x='150', y='300')
        self.canvas_8 = tk.Canvas(self.frame_1_1)
        self.canvas_8.config(background='#000000', height='150', width='150')
        self.canvas_8.place(anchor='nw', height='150', width='150', x='300', y='300')
        self.canvas_9 = tk.Canvas(self.frame_1_1)
        self.canvas_9.config(background='#000000', height='150', relief='flat')
        self.canvas_9.config(width='150')
        self.canvas_9.place(anchor='nw', height='150', width='150', x='0', y='450')
        self.canvas_10 = tk.Canvas(self.frame_1_1)
        self.canvas_10.config(background='#000000', height='150', relief='flat')
        self.canvas_10.config(width='150')
        self.canvas_10.place(anchor='nw', height='150', width='150', x='150', y='450')
        self.canvas_11 = tk.Canvas(self.frame_1_1)
        self.canvas_11.config(background='#000000', confine='false', height='150', relief='flat')
        self.canvas_11.config(width='150')
        self.canvas_11.place(anchor='nw', height='150', width='150', x='300', y='450')
        self.canvas_12 = tk.Canvas(self.frame_1_1)
        self.canvas_12.config(background='#000000', height='150', relief='flat', width='150')
        self.canvas_12.place(anchor='nw', height='150', width='150', x='0', y='150')
        self.frame_1_1.config(height='600', width='450')
        self.frame_1_1.place(anchor='nw', height='600', width='450', x='75', y='75')
        self.frame_1_2 = ttk.Frame(self.frame_1)
        self.canvas_1_1 = tk.Canvas(self.frame_1_2)
        self.canvas_1_1.config(background='#000000', height='200', width='750')
        self.canvas_1_1.place(anchor='nw', height='200', width='750', x='0', y='0')
        self.frame_1_2.config(height='200', width='750')
        self.frame_1_2.place(anchor='nw', height='200', width='750', x='550', y='75')
        self.frame_1_2_3 = ttk.Frame(self.frame_1)
        self.canvas_2_1 = tk.Canvas(self.frame_1_2_3)
        self.canvas_2_1.config(background='#000000', height='168', width='168')
        self.canvas_2_1.place(anchor='nw', height='168', width='168', x='0', y='0')
        self.message_1 = tk.Label(self.frame_1_2_3, font=(None, 20))
        self.message_1.config(background='#000000', foreground='#00ff80')
        self.message_1.config(takefocus=False, text='BPM')
        self.message_1.place(anchor='nw', height='42', width='84', x='82', y='124')
        self.heartrate = tk.Label(self.frame_1_2_3, font=(None, 64))
        self.heartrate.config(background='#000000', foreground='#00ff80')
        self.heartrate.config(takefocus=False, text='--')
        self.heartrate.place(anchor='nw', height='73', width='164', x='2', y='50')
        self.canvas_2_1.pack()
        self.img2 = ImageTk.PhotoImage(Image.open("Heart Rate.png"))      
        self.canvas_2_1.create_image(8,8, anchor=NW, image=self.img2) 
        self.canvas_2_1.image = self.img2
        self.frame_1_2_3.config(height='168', width='168')
        self.frame_1_2_3.place(anchor='nw', height='168', width='168', x='550', y='300')
        self.frame_1_2_3_4 = ttk.Frame(self.frame_1)
        self.canvas_2_3 = tk.Canvas(self.frame_1_2_3_4)
        self.canvas_2_3.config(background='#000000', height='168', width='168')
        self.canvas_2_3.place(anchor='nw', height='168', width='168', x='0', y='0')
        self.message_1_3 = tk.Label(self.frame_1_2_3_4, font=(None, 20))
        self.message_1_3.config(background='#000000', foreground='#ff0000', takefocus=False)
        self.message_1_3.config(text='F')
        self.message_1_3.place(anchor='nw', height='42', width='42', x='124', y='124')
        self.temperature = tk.Label(self.frame_1_2_3_4, font=(None, 64))
        self.temperature.config(background='#000000', foreground='#ff0000')
        self.temperature.config(takefocus=False, text='--')
        self.temperature.place(anchor='nw', height='73', width='164', x='2', y='50')
        self.canvas_2_3.pack()      
        self.img3 = ImageTk.PhotoImage(Image.open("Temprature.png"))      
        self.canvas_2_3.create_image(8,8, anchor=NW, image=self.img3) 
        self.canvas_2_3.image = self.img3
        self.frame_1_2_3_4.config(height='168', width='168')
        self.frame_1_2_3_4.place(anchor='nw', height='168', width='168', x='718', y='300')
        self.frame_1_2_3_4_5 = ttk.Frame(self.frame_1)
        self.canvas_2_4 = tk.Canvas(self.frame_1_2_3_4_5)
        self.canvas_2_4.config(background='#000000', height='168', width='243')
        self.canvas_2_4.place(anchor='nw', height='168', width='243', x='0', y='0')
        self.message_1_4 = tk.Label(self.frame_1_2_3_4_5, font=(None, 20))
        self.message_1_4.config(background='#000000', foreground='#ff8040', takefocus=False)
        self.message_1_4.config(text='KG')
        self.message_1_4.place(anchor='nw', height='42', width='42', x='199', y='124')
        self.weight = tk.Label(self.frame_1_2_3_4_5, font=(None, 40))
        self.weight.config(background='#000000', foreground='#ff8040')
        self.weight.config(takefocus=False, text='-- to --')
        self.weight.place(anchor='nw', height='73', width='239', x='2', y='50')
        self.canvas_2_4.pack()      
        self.img4 = ImageTk.PhotoImage(Image.open("Weight.png"))      
        self.canvas_2_4.create_image(8,8, anchor=NW, image=self.img4) 
        self.canvas_2_4.image = self.img4
        self.frame_1_2_3_4_5.config(height='168', width='243')
        self.frame_1_2_3_4_5.place(anchor='nw', height='168', width='243', x='1054', y='300')
        self.frame_1_2_3_4_5_6 = ttk.Frame(self.frame_1)
        self.canvas_2_5 = tk.Canvas(self.frame_1_2_3_4_5_6)
        self.canvas_2_5.config(background='#000000', height='168', width='168')
        self.canvas_2_5.place(anchor='nw', height='168', width='168', x='0', y='0')
        self.message_1_5 = tk.Label(self.frame_1_2_3_4_5_6, font=(None, 20))
        self.message_1_5.config(background='#000000', foreground='#ffff00', takefocus=False)
        self.message_1_5.config(text='%')
        self.message_1_5.place(anchor='nw', height='42', width='42', x='124', y='124')
        self.urinebag = tk.Label(self.frame_1_2_3_4_5_6, font=(None, 64))
        self.urinebag.config(background='#000000', foreground='#ffff00')
        self.urinebag.config(takefocus=False, text='--')
        self.urinebag.place(anchor='nw', height='73', width='164', x='2', y='50')
        self.canvas_2_5.pack()      
        self.img5 = ImageTk.PhotoImage(Image.open("Urine Bag.png"))      
        self.canvas_2_5.create_image(8,8, anchor=NW, image=self.img5) 
        self.canvas_2_5.image = self.img5
        self.frame_1_2_3_4_5_6.config(height='168', width='168')
        self.frame_1_2_3_4_5_6.place(anchor='nw', height='168', width='168', x='886', y='300')
        self.frame_1_2_7 = ttk.Frame(self.frame_1)
        self.canvas_6_1 = tk.Canvas(self.frame_1_2_7)
        self.canvas_6_1.config(background='#000000', confine='false', height='175', width='750')
        self.canvas_6_1.place(anchor='nw', height='175', width='750', x='0', y='0')
        self.alert = tk.Label(self.frame_1_2_7, font=(None, 24))
        self.alert.config(background='#000000', foreground='#ffffff')
        self.alert.config(takefocus=False, text='Unoccupied')
        self.alert.place(anchor='nw', height='115', width='690', x='58', y='58')
        self.canvas_6_1.pack()      
        self.img6 = ImageTk.PhotoImage(Image.open("Alert.png"))      
        self.canvas_6_1.create_image(8,8, anchor=NW, image=self.img6) 
        self.canvas_6_1.image = self.img6
        self.frame_1_2_7.config(height='175', width='750')
        self.frame_1_2_7.place(anchor='nw', height='175', width='750', x='550', y='493')
        self.frame_1.config(cursor='based_arrow_up', height='768', width='1366')
        self.frame_1.place(anchor='nw', height='768', width='1366', x='0', y='0')

        self.mainwindow = self.frame_1
        self.update()


    def run(self):
        self.mainwindow.mainloop()
        
        
    def update(self):
        if (not testing):
            weightValues = serialWeight.readline().decode()
        else:
            weightValues = "<" + str(random.randint(0, 150)) + "," + str(random.randint(0, 150)) + "," + str(random.randint(0, 150)) + "," + str(random.randint(0, 150)) + "," + str(random.randint(0, 150)) + "," + str(random.randint(0, 150)) + "," + str(random.randint(0, 150)) + "," + str(random.randint(0, 150)) + "," + str(random.randint(0, 150)) + "," + str(random.randint(0, 150)) + "," + str(random.randint(0, 150)) + "," + str(random.randint(0, 150)) + "," + str(random.randint(0, 150)) + " to " + str(random.randint(0, 150)) + ">"
        print(weightValues)
        if (weightValues[0] == '<'):
            weightValues = np.array(weightValues.split(","))
            wt = weightValues[12].replace(">", "")
            self.weight.configure(text=wt)
            diff = int((float(weightValues[0].replace("<", "")) / 150.0) * 255.0)
            if (diff < 0):
                diff = 0
            hexVal = hex(diff).lstrip("0x").rstrip("L")
            if (len(hexVal) == 1):
                hexVal = "0" + hexVal
            elif (len(hexVal) == 0):
                hexVal = "00"
            elif (len(hexVal) == 3):
                hexVal = "ff"
            color1 = "#" + hexVal + "0000"
            self.canvas_1.config(background=color1)
            diff = int((float(weightValues[1]) / 150.0) * 255.0)
            if (diff < 0):
                diff = 0
            hexVal = hex(diff).lstrip("0x").rstrip("L")
            if (len(hexVal) == 1):
                hexVal = "0" + hexVal
            elif (len(hexVal) == 0):
                hexVal = "00"
            elif (len(hexVal) == 3):
                hexVal = "ff"
            color2 = "#" + hexVal + "0000"
            self.canvas_2.config(background=color2)
            diff = int((float(weightValues[2]) / 150.0) * 255.0)
            if (diff < 0):
                diff = 0
            hexVal = hex(diff).lstrip("0x").rstrip("L")
            if (len(hexVal) == 1):
                hexVal = "0" + hexVal
            elif (len(hexVal) == 0):
                hexVal = "00"
            elif (len(hexVal) == 3):
                hexVal = "ff"
            color3 = "#" + hexVal + "0000"
            self.canvas_3.config(background=color3)
            diff = int((float(weightValues[3]) / 150.0) * 255.0)
            if (diff < 0):
                diff = 0
            hexVal = hex(diff).lstrip("0x").rstrip("L")
            if (len(hexVal) == 1):
                hexVal = "0" + hexVal
            elif (len(hexVal) == 0):
                hexVal = "00"
            elif (len(hexVal) == 3):
                hexVal = "ff"
            color4 = "#" + hexVal + "0000"
            self.canvas_4.config(background=color4)
            diff = int((float(weightValues[4]) / 150.0) * 255.0)
            if (diff < 0):
                diff = 0
            hexVal = hex(diff).lstrip("0x").rstrip("L")
            if (len(hexVal) == 1):
                hexVal = "0" + hexVal
            elif (len(hexVal) == 0):
                hexVal = "00"
            elif (len(hexVal) == 3):
                hexVal = "ff"
            color5 = "#" + hexVal + "0000"
            self.canvas_5.config(background=color5)
            diff = int((float(weightValues[5]) / 150.0) * 255.0)
            if (diff < 0):
                diff = 0
            hexVal = hex(diff).lstrip("0x").rstrip("L")
            if (len(hexVal) == 1):
                hexVal = "0" + hexVal
            elif (len(hexVal) == 0):
                hexVal = "00"
            elif (len(hexVal) == 3):
                hexVal = "ff"
            color6 = "#" + hexVal + "0000"
            self.canvas_6.config(background=color6)
            diff = int((float(weightValues[6]) / 150.0) * 255.0)
            if (diff < 0):
                diff = 0
            hexVal = hex(diff).lstrip("0x").rstrip("L")
            if (len(hexVal) == 1):
                hexVal = "0" + hexVal
            elif (len(hexVal) == 0):
                hexVal = "00"
            elif (len(hexVal) == 3):
                hexVal = "ff"
            color7 = "#" + hexVal + "0000"
            self.canvas_7.config(background=color7)
            diff = int((float(weightValues[7]) / 150.0) * 255.0)
            if (diff < 0):
                diff = 0
            hexVal = hex(diff).lstrip("0x").rstrip("L")
            if (len(hexVal) == 1):
                hexVal = "0" + hexVal
            elif (len(hexVal) == 0):
                hexVal = "00"
            elif (len(hexVal) == 3):
                hexVal = "ff"
            color8 = "#" + hexVal + "0000"
            self.canvas_8.config(background=color8)
            diff = int((float(weightValues[8]) / 150.0) * 255.0)
            if (diff < 0):
                diff = 0
            hexVal = hex(diff).lstrip("0x").rstrip("L")
            if (len(hexVal) == 1):
                hexVal = "0" + hexVal
            elif (len(hexVal) == 0):
                hexVal = "00"
            elif (len(hexVal) == 3):
                hexVal = "ff"
            color9 = "#" + hexVal + "0000"
            self.canvas_9.config(background=color9)
            diff = int((float(weightValues[9]) / 150.0) * 255.0)
            if (diff < 0):
                diff = 0
            hexVal = hex(diff).lstrip("0x").rstrip("L")
            if (len(hexVal) == 1):
                hexVal = "0" + hexVal
            elif (len(hexVal) == 0):
                hexVal = "00"
            elif (len(hexVal) == 3):
                hexVal = "ff"
            color10 = "#" + hexVal + "0000"
            self.canvas_10.config(background=color10)
            diff = int((float(weightValues[10]) / 150.0) * 255.0)
            if (diff < 0):
                diff = 0
            hexVal = hex(diff).lstrip("0x").rstrip("L")
            if (len(hexVal) == 1):
                hexVal = "0" + hexVal
            elif (len(hexVal) == 0):
                hexVal = "00"
            elif (len(hexVal) == 3):
                hexVal = "ff"
            color11 = "#" + hexVal + "0000"
            self.canvas_11.config(background=color11)
            diff = int((float(weightValues[11]) / 150.0) * 255.0)
            if (diff < 0):
                diff = 0
            hexVal = hex(diff).lstrip("0x").rstrip("L")
            if (len(hexVal) == 1):
                hexVal = "0" + hexVal
            elif (len(hexVal) == 0):
                hexVal = "00"
            elif (len(hexVal) == 3):
                hexVal = "ff"
            color12 = "#" + hexVal + "0000"
            self.canvas_12.config(background=color12)
        if (not testing):
            tempValue = serialTemp.readline().decode().replace("\r\n", "")
        else:
            tempValue = random.randint(98, 110)
        if (tempValue == "--"):
            tp = tempValue
        else:
            tp = str(int(float(tempValue)))
        self.temperature.configure(text=tp)
        self.mainwindow.after(42, self.update)


if __name__ == '__main__':
    import tkinter as tk
    if (not testing):
        serialTemp = serial.Serial('COM6', 9600)
        serialWeight = serial.Serial('COM4', 9600)
    root = tk.Tk()
    app = UserinterfaceApp(root)
    app.run()
