from datetime import datetime
from pytides.tide import Tide
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


##Prepare our tide data
station_id = 'Fernandina Beach'

columns = ['time', 'data']
heights = []
t = []
data = pd.read_csv('/Users/anonymous/clawpack_src/clawpack-v5.4.1rc-beta/geoclaw/examples/storm-surge/matthew/detide/data/FernandinaBeach.csv', header=None, names=columns)

for x in data.time:
    if (x != 'time'):
        datetime_object = datetime.strptime(x, '%x  %H:%M')
        t.append(datetime_object)

for y in data.data:
    if (y != 'data'):
        heights.append(float(y))
#print heights
#print t

#For a quicker decomposition, we'll only use hourly readings rather than 6-minutely readings.
# heights = np.array(heights[::10])
# t = np.array(t[::10])

##Prepare a list of datetimes, each 6 minutes apart, for a week.
prediction_t0 = datetime(2016,10,4)
hours = np.arange(6 * 24)
times = Tide._times(prediction_t0, hours)
# print times

##Fit the tidal data to the harmonic model using Pytides
my_tide = Tide.decompose(heights, t)
##Predict the tides using the Pytides model.
my_prediction = my_tide.at(times)

##Prepare NOAA's results
noaa_verified = []
noaa_predicted = []

column = ['time', 'prediction', 'verified']
result = pd.read_csv('/Users/anonymous/clawpack_src/clawpack-v5.4.1rc-beta/geoclaw/examples/storm-surge/matthew/detide/data/FernandinaBeach_noaa.csv', header=None, names=column)
for x in result.prediction:
    if (x != 'prediction'):
    	print x
        noaa_predicted.append(float(y))
for y in result.verified:
    if (y != 'verified'):
        noaa_verified.append(float(y))

#print noaa_predicted

##Plot the results
plt.plot(hours, my_prediction, label="Pytides")
plt.plot(hours, noaa_predicted, label="NOAA Prediction")
plt.plot(hours, noaa_verified, label="NOAA Verified")
plt.legend()
plt.title('Comparison of Pytides and NOAA predictions for Station: ' + str(station_id))
plt.xlabel('Hours since ' + str(prediction_t0) + '(GMT)')
plt.ylabel('Metres')

plt.show()
