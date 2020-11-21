import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial
#import numpy.random as random


# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
ser = serial.Serial('COM4', 9600)
extra = []
c = []

initial = [[0,0,0],[0,0,0],[0,0,0],[0,0,0]]

firstTime = True

def show_values(pc, fmt="E%d = %.2f\nDiff = %.2f\n%s", **kw):
    '''
    Heatmap with text in each cell with matplotlib's pyplot
    Source: http://stackoverflow.com/a/25074150/395857 
    By HYRY
    '''
    pc.update_scalarmappable()
    ax = pc.axes
    Elist = [1,2,3,4,5,6,7,8,9,10,11,12]
    for p, color, diff, E in zip(pc.get_paths(), pc.get_facecolors(), pc.get_array(), Elist):
        x, y = p.vertices[:-2, :].mean(0)
        if np.all(color[:3] > 0.5):
            color = (0.0, 0.0, 0.0)
        else:
            color = (1.0, 1.0, 1.0)
        
        val, extra[E-1] = extra[E-1].split('(')
        extra[E-1] = extra[E-1][ : extra[E-1].find("-")] + 'uA' + extra[E-1][extra[E-1].find("-") : extra[E-1].find(")")] + 'uS'
        ax.text(x, y, fmt % (E, float(val), diff, extra[E-1]), ha="center", va="center", color=color, **kw)

def heatmap(AUC):
    '''
    Inspired by:
    - http://stackoverflow.com/a/16124677/395857 
    - http://stackoverflow.com/a/25074150/395857
    '''
    global ax, fig , firstTime, initial, c
    
    if(firstTime):
        x_axis_size = AUC.shape[1]
        y_axis_size = AUC.shape[0]
        title = "MPR121 data"
        xlabel= "ROW"
        ylabel="COL"
        xticklabels = range(1, x_axis_size+1) # could be text
        yticklabels = range(1, y_axis_size+1) # could be text 
        fig.tight_layout()
    ax.clear()

    # Plot it out
#     if(firstTime):
    c = ax.pcolor( initial-AUC, edgecolors='k', linestyle= 'dashed', linewidths=0.2, cmap='magma_r', vmin=0.0, vmax=1023.0)
#     else:
#         c.set_data(AUC)
    
    # Add color bar
    if(firstTime):
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
        initial = AUC
        plt.colorbar(c)
        firstTime = False
        
    # Add text in each cell 
    show_values(c)    

def readSerial():
    global serial
    global extra
    try:
        # Read and record the data
        data =[]                       # empty list to store the data
        extra = ser.readline().decode().rstrip().split("\t")
#         extra = [str(random.randint(0, 1000)) + '(55-0.50)', str(random.randint(0, 1000)) + '(54-0.50)', str(random.randint(0, 1000)) + '(52-0.50)', str(random.randint(0, 1000)) + '(51-0.50)', str(random.randint(0, 1000)) + '(51-0.50)', str(random.randint(0, 1000)) + '(51-0.50)', str(random.randint(0, 1000)) + '(51-0.50)', str(random.randint(0, 1000)) + '(50-0.50)', str(random.randint(0, 1000)) + '(52-0.50)', str(random.randint(0, 1000)) + '(54-0.50)', str(random.randint(0, 1000)) + '(55-0.50)', str(random.randint(0, 1000)) + '(57-0.50)']
    
        for e in extra:
            data.append(e.split('(')[0])
    
        #return np.array([data[:2]], dtype='float').reshape(1,2)   
        return np.array([data], dtype='float').reshape(4,3)
    except:
        return np.zeros((4,3), dtype="float")

def animate(i):

    data = readSerial()  
    heatmap(data)
    return c
  

# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, frames=10, interval=300)
plt.show()
ser.close()
