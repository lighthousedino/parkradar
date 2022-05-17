import numpy as np
import random
import sys, os
import csv
import pandas as pd

sys.path.append('/path/to/parkradar')

from parking.recommend import now

#file = open("Phoenix addressess.csv")
#csvreader = csv.reader(file)
#data = []
#for row in csvreader:
#    data.append(str(row))
#data = np.squeeze(data)
#data = np.squeeze(data)
#print(data)
data = pd.read_csv("Phoenix addressess.csv", header = None)
#data = data.splitlines()
#data = np.genfromtxt("Phoenix addressess.csv").splitlines()
print(data)


def predict(num_iters):
  days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
  time = ()
  distance = ()
  cure_location = ()
  for i in range(0, num_iters):
    
    location2 = data.iloc[random.randint(0, len(data)), 0]
    phoenix = ", Phoenix"
    location = location2 + phoenix
    day = random.randint(0, 6)
    day = days[day]
    time = str(random.randint(0, 24))
    time2 = ":00"
    hour = time + time2
    print(day, hour, location)
    
    recommendation = now(location, day, hour)
    
    cure_location.append(location2)
    time.append(recommendation["estimated_distance"])
    distance.append(recommendation["estimated_time"])
    
  #data = np.column_stack(cure_location, time)
  #data = np.column_stack(data, distance)
    
  return cure_location, time, distance

cure_location, time, distance = predict(1000)
np.savetxtx("Model_data.csv", (cure_location, time, distance), delimiter = ',')



