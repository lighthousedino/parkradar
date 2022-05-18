import numpy as np
import random
import pandas as pd
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
#print(data)


def predict(num_iters):
  days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
  matrix = np.zeros((num_iters, 3), dtype =np.dtype('U100'))
  for i in range(0, num_iters):
    
    location2 = data.iloc[random.randint(0, len(data)-1), 0]
    phoenix = ", Phoenix"
    location = location2 + phoenix
    day = random.randint(0, 6)
    day = days[day]
    time = str(random.randint(0, 24))
    time2 = ":00"
    hour = time + time2
    #print(day, hour, location)
    
    recommendation = now(location, day, hour)
    print(location, recommendation["estimated_distance"], recommendation["estimated_time"])
    matrix[i, 0] = location
    matrix[i, 1] = recommendation["estimated_distance"]
    matrix[i, 2] = recommendation["estimated_time"]
    
  #data = np.column_stack(cure_location, time)
  #data = np.column_stack(data, distance)
    
  return matrix

matrix = predict(1000)
print(matrix)
np.savetxt("Model_data.csv", matrix, delimiter = ',', fmt = '%s')



