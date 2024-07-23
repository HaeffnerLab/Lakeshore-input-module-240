from lakeshore import Model240, Model240InputParameter
from time import sleep
import csv, datetime
from itertools import count
import random


TIME_INCREMENT = 1 #in seconds
test = False

FILENAME = "test.csv"

def setFilename(name):
    global FILENAME
    FILENAME = name

def setTimeIncrement(num):
    global TIME_INCREMENT
    TIME_INCREMENT = num

"""FILE STUFF"""
def writeFile():
    global FILENAME
    #begin writing file
    fields = ['Time (s)', 'Channel 1 (V)', 'Channel 1 (K)', 'Channel 2 (V)', 'Channel 2 (K)']

    with open(FILENAME, 'w') as csvfile:
        #creating a csv writer object
        csvwriter = csv.writer(csvfile, lineterminator = '\n')
        #writing the fields
        csvwriter.writerow(fields)

#updating file
def updateFile (filename, row):
    with open(filename, 'a') as csvfile:
        csvwriter = csv.writer(csvfile, lineterminator = '\n')
        csvwriter.writerow(row)


"""DATA COLLECTION"""
index = count()

def collectData():
    time = next(index) * TIME_INCREMENT
    ch1V = random.randint(0,10)
    ch1K = random.randint(0,10)
    ch2V = random.randint(0,10)
    ch2K = random.randint(0,10)
    row = [time, ch1V, ch1K, ch2V, ch2K]
    updateFile(FILENAME, row)

if (not test):
    # Connect to the first available Model 240 over USB
    my_model_240 = Model240()

    # Define the channel configuration for a sensor with a negative temperature coefficient, autorange disabled
    # current reversal disabled, the channel enabled, and set to the 100 kOhm range
    rtd_config = Model240InputParameter(my_model_240.SensorTypes.DIODE, False, False, my_model_240.Units.KELVIN, True,
                                        my_model_240.InputRange.RANGE_DIODE)

    # Apply the configuration to all channels
    for channel in range(1, 3):
        my_model_240.set_input_parameter(channel, rtd_config)

    sleep(1)

    def collectData():
        time = next(index) * TIME_INCREMENT
        ch1V = my_model_240.get_sensor_reading(1)
        ch1K = my_model_240.get_kelvin_reading(1)
        ch2V = my_model_240.get_sensor_reading(2)
        ch2K = my_model_240.get_kelvin_reading(2)

        row = [time, ch1V, ch1K, ch2V, ch2K]
        updateFile(FILENAME, row)