import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ser = serial.Serial('COM6', 9600)

firstTime = True

def show_values(pc, fmt="E%d = %.2f", **kw):
    '''
    Heatmap with text in each cell with matplotlib's pyplot
    Source: http://stackoverflow.com/a/25074150/395857 
    By HYRY
    '''
    pc.update_scalarmappable()
    ax = pc.axes
    Elist = [1,2,3,4,5,6,7,8,9,10,11,12]
    for p, color, value, E in zip(pc.get_paths(), pc.get_facecolors(), pc.get_array(), Elist):
        x, y = p.vertices[:-2, :].mean(0)
        if np.all(color[:3] > 0.5):
            color = (0.0, 0.0, 0.0)
        else:
            color = (1.0, 1.0, 1.0)
        ax.text(x, y, fmt % (E, value), ha="center", va="center", color=color, **kw)

def cm2inch(*tupl):
    '''
    Specify figure size in centimeter in matplotlib
    Source: http://stackoverflow.com/a/22787457/395857
    By gns-ank
    '''
    inch = 2.54
    if type(tupl[0]) == tuple:
        return tuple(i/inch for i in tupl[0])
    else:
        return tuple(i/inch for i in tupl)

def heatmap(AUC, title, xlabel, ylabel, xticklabels, yticklabels):
    '''
    Inspired by:
    - http://stackoverflow.com/a/16124677/395857 
    - http://stackoverflow.com/a/25074150/395857
    '''
    global ax, fig , firstTime
    fig.tight_layout()
    ax.clear()

    # Plot it out
    MAX = np.max(AUC)
    MIN = np.min(AUC)
    c = ax.pcolor(AUC, edgecolors='k', linestyle= 'dashed', linewidths=0.2, cmap='magma', vmin=500.0, vmax=750.0)

    # put the major ticks at the middle of each cell
    ax.set_yticks(np.arange(AUC.shape[0]) + 0.5, minor=False)
    ax.set_xticks(np.arange(AUC.shape[1]) + 0.5, minor=False)

    # set tick labels
    ax.set_xticklabels(np.arange(1,AUC.shape[1]+1), minor=False)
    ax.set_xticklabels(xticklabels, minor=False)
    ax.set_yticklabels(yticklabels, minor=False)

    # set title and x/y labels
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    ax.invert_yaxis()  
    
    # Add color bar
    if(firstTime):
        plt.colorbar(c)
        firstTime = False

    # Add text in each cell 
    show_values(c)

    # resize 
    fig = plt.gcf()
    fig.set_size_inches(cm2inch(15, 15))
    


def readSerial():
    global serial
    try:
        
        # Read and record the data
        data =[]                       # empty list to store the data
        
        b = ser.readline()         # read a byte string
        string_n = b.decode()  # decode byte string into Unicode  
        string = string_n.rstrip() # remove \n and \r
        data = string.split("\t")

        #return np.array([data[:2]], dtype='float').reshape(1,2)   
        return np.array([data], dtype='float').reshape(4,3)
    except:
        return np.zeros((4,3), dtype="float")

def animate(i):

    data = readSerial()
    #data = np.random.randint(0,1023,(4,3))##

    x_axis_size = data.shape[1]
    y_axis_size = data.shape[0]
    title = "MPR121 data"
    xlabel= "ROW"
    ylabel="COL"
    xticklabels = range(1, x_axis_size+1) # could be text
    yticklabels = range(1, y_axis_size+1) # could be text   
    heatmap(data, title, xlabel, ylabel, xticklabels, yticklabels)
  

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, interval=50)
plt.show()
ser.close()