import numpy as np
import googlemaps
from garages import registered_garages
from garages.predict import predict_occupancy, simulate_sensors
from parking.recommend import now
from parkradar import Phoenix addressess as Pa



def predict(num_iters):
  data = ()
  for i in range(0, num_iters):
    
    location = Pa[random.randint(0, 2700)]
    day = random.randint(0, 6)
    hour = random.randint(0, 24)
    
    data.append(now(location, day, hour))
    
    return data
  

