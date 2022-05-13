from keras import models
import random
import numpy as np
import pathlib
from . import registered_garages


CURRENT_DIRECTORY = pathlib.Path(__file__).parent.resolve()
REGISTERED_GARAGES = registered_garages.REGISTERED_GARAGES
DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
HMS = [60*60, 60, 1]
TZ_DIFF = 8 # Brisbane is 8 hours ahead of NL


def predict_occupancy(garage_name, day, time):
    '''
    Returns a predicted occupancy ratio of the garage given the day and time.
    Prediction is done using Keras model associated with that garage as
    specified in registered_garages.py
    '''
    garage = next((item for item in REGISTERED_GARAGES if item['name'] == garage_name), None)
    model_path = f'{CURRENT_DIRECTORY}/models/{garage["model"]}'
    model = models.load_model(model_path)

    input_day = DAYS.index(day)
    input_time = sum(a * b for a,b in zip(HMS, map(int, time.split(':'))))
    input_time /= 3600.

    # convert Brisbane time to Netherlands time
    input_time += TZ_DIFF
    if input_time >= 24:
        input_time -= 24
        input_day += 1
        if input_day > 6:
            input_day = 0

    input = np.array([
        input_day,
        input_time
    ]).reshape(1, 2)
    prediction = np.ravel(model(input))[0]

    return prediction


def simulate_sensors(garage_name, day, time):
    '''
    Returns fake data from the 'sensors' at a particular garage at a certain
    day and time. This function just calls predicts() and adds some randomness
    to the output.
    '''
    prediction = predict_occupancy(garage_name, day, time)
    prediction += random.uniform(-0.1, 0.1)
    prediction += (np.random.normal(loc=0.5, scale=0.1, size=None))*0.1
    if prediction > 1:
        prediction == 0.95
    if prediction < 0:
        prediction == 0.05

    return prediction
