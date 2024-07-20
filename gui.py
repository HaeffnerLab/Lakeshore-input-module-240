import tkinter as tk
from tkinter import ttk

from matplotlib.figure import Figure 
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import datetime
from time import sleep
import CollectingData

FILENAME = "test.csv"
TIME_INCREMENT = 1

window = tk.Tk(className="LakeShore Temperature Sensor")
window.geometry('700x700')

"""SETING UP FILE"""
def beginCollecting():
    global FILENAME

    t = datetime.datetime.now()
    t = t.replace(microsecond=0)
    t = str(t).replace(":", ".")
    FILENAME = t + '.csv'
    CollectingData.setFilename(FILENAME)
    CollectingData.setTimeIncrement(TIME_INCREMENT)
    CollectingData.writeFile()


"""GRAPH"""
style.use('ggplot')
f = Figure(figsize=(5,5), dpi=100)
plt = f.add_subplot(111)

def animate(i):
    """'loop' for data collection"""
    if (isRunning):
        #CollectingData.collectData()
        CollectingData.testCollect()

    pullData = open(FILENAME,"r").read()
    dataList = pullData.split('\n')
    dataList.pop(0)
    timeList = []
    ch1VList = []
    ch1KList=[]
    ch2VList = []
    ch2KList = []
    for index in range(1, min(11, len(dataList))):
        line = dataList[len(dataList) - index]
        if (len(line) > 1):
            vals = line.split(',')
            timeList.insert(0, float(vals[0]))
            ch1VList.insert(0, float(vals[1]))
            ch1KList.insert(0, float(vals[2]))
            ch2VList.insert(0, int(vals[3]))
            ch2KList.insert(0, int(vals[4]))

    plt.clear()

    if (chChoosen.get() == ' Channel 1'):
        if (len(ch1KList) > 0 ):
            temp.set(str(ch1KList[len(ch1KList)-1]) + "K")
        plt.plot(timeList, ch1VList, label="voltage (V)")
        plt.plot(timeList, ch1KList, label="temperature (K)")

    if (chChoosen.get() == ' Channel 2'):
        if (len(ch2KList) > 0 ):
            temp.set(str(ch2KList[len(ch2KList)-1]) + "K")
        plt.plot(timeList, ch2VList, label="voltage (V)")
        plt.plot(timeList, ch2KList, label="temperature (K)")
    
    plt.legend(loc="upper right")

canvas = FigureCanvasTkAgg(f, window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
    


"""START BUTTON"""
isRunning = False
def clickButton():
    global isRunning
    if isRunning:
        isRunning = False
        button.config(text="START", bg="lightblue")
    else:
        isRunning = True
        button.config(text="STOP", bg="red")
        beginCollecting()

button = tk.Button(window, text="START", command=clickButton, height=3, width=15, bg="lightblue")
button.place(x=20, y=20)


"""TEMPERATURE LABEL"""
temp = tk.StringVar()
temp.set("0.0K")
tempLabel = tk.Label(window, textvariable=temp, bd=0, font=("Arial", 40), bg="white")
tempLabel.place(x=500, y=20)


"""COMBOBOX FOR SELECTING CHANNEL"""
chLabel = tk.Label(window, text="Channel:", font=("Arial", 10), bg="white")
chLabel.place(x=190, y=25)
n = tk.StringVar()
chChoosen = ttk.Combobox(window, width=27, textvariable=n)
chChoosen['values'] = (' Channel 1', ' Channel 2')
chChoosen.current(0)
chChoosen.place(x=250, y=25)


ani = animation.FuncAnimation(f, animate, interval = 1000 * TIME_INCREMENT, cache_frame_data=False)
window.mainloop()