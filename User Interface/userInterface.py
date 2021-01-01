import tkinter as tk
import tkinter.ttk as ttk


class UserinterfaceApp:
    def __init__(self, master=None):
        # build ui
        self.frame_1 = ttk.Frame(master)
        self.canvas_1_1_1 = tk.Canvas(self.frame_1)
        self.canvas_1_1_1.config(background='#000000', confine='true', height='768', relief='raised')
        self.canvas_1_1_1.config(width='1366')
        self.canvas_1_1_1.place(anchor='nw', height='768', width='1366', x='0', y='0')
        self.frame_1_1 = ttk.Frame(self.frame_1)
        self.canvas_1_1 = tk.Canvas(self.frame_1_1)
        self.canvas_1_1.config(background='#800000', confine='true', height='150', relief='flat')
        self.canvas_1_1.config(width='150')
        self.canvas_1_1.place(anchor='nw', height='150', width='150', x='0', y='0')
        self.canvas_3_2 = tk.Canvas(self.frame_1_1)
        self.canvas_3_2.config(background='#800000', cursor='arrow', height='150', width='150')
        self.canvas_3_2.place(anchor='nw', height='150', width='150', x='150', y='0')
        self.canvas_4_3 = tk.Canvas(self.frame_1_1)
        self.canvas_4_3.config(background='#800000', height='150', width='150')
        self.canvas_4_3.place(anchor='nw', height='150', width='150', x='300', y='0')
        self.canvas_6_4 = tk.Canvas(self.frame_1_1)
        self.canvas_6_4.config(background='#800000', height='150', width='150')
        self.canvas_6_4.place(anchor='nw', height='150', width='150', x='150', y='150')
        self.canvas_7_5 = tk.Canvas(self.frame_1_1)
        self.canvas_7_5.config(background='#800000', height='150', relief='flat', width='150')
        self.canvas_7_5.place(anchor='nw', height='150', width='150', x='300', y='150')
        self.canvas_8_6 = tk.Canvas(self.frame_1_1)
        self.canvas_8_6.config(background='#800000', height='150', relief='flat', width='150')
        self.canvas_8_6.place(anchor='nw', height='150', width='150', x='0', y='300')
        self.canvas_9_7 = tk.Canvas(self.frame_1_1)
        self.canvas_9_7.config(background='#800000', height='150', takefocus=False, width='150')
        self.canvas_9_7.place(anchor='nw', height='150', width='150', x='150', y='300')
        self.canvas_10_8 = tk.Canvas(self.frame_1_1)
        self.canvas_10_8.config(background='#800000', height='150', width='150')
        self.canvas_10_8.place(anchor='nw', height='150', width='150', x='300', y='300')
        self.canvas_11_9 = tk.Canvas(self.frame_1_1)
        self.canvas_11_9.config(background='#800000', cursor='arrow', height='150', relief='flat')
        self.canvas_11_9.config(width='150')
        self.canvas_11_9.place(anchor='nw', height='150', width='150', x='0', y='450')
        self.canvas_12_10 = tk.Canvas(self.frame_1_1)
        self.canvas_12_10.config(background='#800000', cursor='arrow', height='150', relief='flat')
        self.canvas_12_10.config(width='150')
        self.canvas_12_10.place(anchor='nw', height='150', width='150', x='150', y='450')
        self.canvas_14_11 = tk.Canvas(self.frame_1_1)
        self.canvas_14_11.config(background='#800000', confine='false', height='150', relief='flat')
        self.canvas_14_11.config(width='150')
        self.canvas_14_11.place(anchor='nw', height='150', width='150', x='300', y='450')
        self.canvas_5_12 = tk.Canvas(self.frame_1_1)
        self.canvas_5_12.config(background='#800000', height='150', relief='flat', width='150')
        self.canvas_5_12.place(anchor='nw', height='150', width='150', x='0', y='150')
        self.frame_1_1.config(height='600', width='450')
        self.frame_1_1.place(anchor='nw', height='600', width='450', x='84', y='84')
        self.frame_1.config(cursor='based_arrow_up', height='768', width='1366')
        self.frame_1.place(anchor='nw', height='768', width='1366', x='0', y='0')

        # Main widget
        self.mainwindow = self.frame_1


    def run(self):
        self.mainwindow.mainloop()

if __name__ == '__main__':
    import tkinter as tk
    root = tk.Tk()
    app = UserinterfaceApp(root)
    app.run()

