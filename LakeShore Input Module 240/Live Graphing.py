# https://www.youtube.com/watch?v=Ercd-Ip5PfQ

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


#VARIABLES
TIME_INCREMENT = 30 #in seconds
FILENAME = 'temp data.csv'
#WINDOW_X = 10  #in inches
#WINDOW_Y = 8  #in inches
#GRAPH_TIME_RANGE = 50 #how much data graph shows
#GRAPH_TEMP_RANGE = 300


plt.style.use('fivethirtyeight')

x_vals = []
y_vals = []

def animate(i):
    data = pd.read_csv(FILENAME)
    x = data['Time (s)']
    #y1 = data['Channel 1 (K)']
    y1 = data['Channel 1 (V)']
    #y2 = data['Channel 2 (K)']
    y2 = data['Channel 2 (V)']

    plt.cla()

    plt.plot(x, y1, label='Ch 1')
    plt.plot(x, y2, label='Ch 2')
    plt.title('Cryo Temperature')
    plt.xlabel('Time (s)')
    plt.ylabel('Temperature (K)')

    temp, y1pt, y2pt = x[len(x) - 1], y1[len(y1) - 1], y2[len(y2) - 1]
    label1 = "{:.2f}".format(y1pt)
    label2 = "{:.2f}".format(y2pt)
    plt.annotate(label1, (temp, y1pt), textcoords='offset points', xytext=(0,10), ha='center')
    plt.annotate(label2, (temp, y2pt), textcoords='offset points', xytext=(0,10), ha='center')

    plt.legend(loc='upper left')
    plt.tight_layout()


ani = FuncAnimation(plt.gcf(), animate, interval=1000*TIME_INCREMENT, cache_frame_data=False)

plt.tight_layout()
plt.show()