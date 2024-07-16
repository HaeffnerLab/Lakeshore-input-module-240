from lakeshore import Model240, Model240InputParameter
from time import sleep
import csv, datetime
from itertools import count

TIME_INCREMENT = 30 #in seconds
time = datetime.datetime.now()
time = time.replace(microsecond=0)
time = str(time).replace(":", ".")
FILENAME = time + '.csv'

#begin writing file
fields = ['Time (s)', 'Channel 1 (V)', 'Channel 1 (K)', 'Channel 2 (V)', 'Channel 2 (K)']

with open(FILENAME, 'w') as csvfile:
    #creating a csv writer object
    csvwriter = csv.writer(csvfile, lineterminator = '\n')
    #writing the fields
    csvwriter.writerow(fields)


### SETTING UP CONFIG
# Connect to the first available Model 240 over USB
my_model_240 = Model240()

# Define the channel configuration for a sensor with a negative temperature coefficient, autorange disabled
# current reversal disabled, the channel enabled, and set to the 100 kOhm range
rtd_config = Model240InputParameter(my_model_240.SensorTypes.NTC_RTD, False, False, my_model_240.Units.SENSOR, True,
                                    my_model_240.InputRange.RANGE_NTCRTD_100_KIL_OHMS)

# Apply the configuration to all channels
for channel in range(1, 3):
    my_model_240.set_input_parameter(channel, rtd_config)

sleep(1)


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


#DATA COLLECTION
def collectData():
    index = count()
    while (True):
        time = next(index) * TIME_INCREMENT
        ch1V = my_model_240.get_sensor_reading(1)
        ch1K = my_model_240.get_kelvin_reading(1)
        ch2V = my_model_240.get_sensor_reading(2)
        ch2K = my_model_240.get_kelvin_reading(2)

        row = [time, ch1V, ch1K, ch2V, ch2K]
        updateFile(FILENAME, row)

        sleep(TIME_INCREMENT)

def testCollect():
    index1 = count()
    index2 = count()
    index3 = count()
    index4 = count()
    index5 = count()
    while (True):
        time = next(index1) * TIME_INCREMENT
        ch1V = next(index2)
        ch1K = next(index3) * 2
        ch2V = next(index4) + 1
        ch2K = next(index5) * 2 + 1

        row = [time, ch1V, ch1K, ch2V, ch2K]
        updateFile(FILENAME, row)

        sleep(TIME_INCREMENT)

#collectData()
testCollect()