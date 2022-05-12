import numpy as np
import googlemaps
from garages import registered_garages
from garages.predict import predict_occupancy, simulate_sensors


REGISTERED_GARAGES = registered_garages.REGISTERED_GARAGES
gmaps = googlemaps.Client(key='AIzaSyBcqvNCEaFN8cgF2_f0038uKWBN038QKYE')


def now(location_from, day, time):
    '''
    Returns the garage with the shortest travel duration from location_from.
    If the garage is more than 90% occupied (based on fake sensor data), returns
    the next best alternative.
    '''
    garages = np.array(REGISTERED_GARAGES)
    rank_duration = []
    for i in garages:
        distance = gmaps.distance_matrix(location_from, i['address'], units='imperial')['rows'][0]['elements'][0]
        rank_duration.append(distance['duration']['value'])
    sorted_indices = np.argsort(rank_duration)

    for i in range(len(sorted_indices)):
        recommendation = garages[sorted_indices[i]]
        distance = gmaps.distance_matrix(location_from, recommendation['address'], units='imperial')['rows'][0]['elements'][0]
        recommendation['estimated_distance'] = distance['distance']['text']
        recommendation['estimated_time'] = distance['duration']['text']

        # use prediction value instead of sensor value if the travel duration is longer thann 15 mins
        if distance['distance']['value'] > 900:
            recommendation['percentage_occupied'] = round(predict_occupancy(recommendation['name'], day, time) * 100)
        else:
            recommendation['percentage_occupied'] = round(simulate_sensors(recommendation['name'], day, time) * 100)

        if recommendation['percentage_occupied'] >= 90 and i != len(sorted_indices):
            continue
        else:
            break

    return recommendation


def ahead(location_from, day, time):
    '''
    Similar to the function 'now' but returns best 3 and uses prediction values instead of sensors
    '''
    garages = np.array(REGISTERED_GARAGES)
    rank_duration = []
    for i in garages:
        distance = gmaps.distance_matrix(location_from, i['address'], units='imperial')['rows'][0]['elements'][0]
        rank_duration.append(distance['duration']['value'])
    sorted_indices = np.argsort(rank_duration)
    garages = garages[sorted_indices] # sorted list of all garages; closest first

    for i in garages:
        i['percentage_occupied'] = round(predict_occupancy(i['name'], day, time) * 100)
    
    # move down the list if more than 90% occupied
    c = 0
    for i in garages:
        if i['percentage_occupied'] >= 90 and garages[-1] != i:
            temp1 = garages[c]
            temp2 = garages[c+1]
            garages[c] = temp2
            garages[c+1] = temp1
        c += 1
    
    recommendations = garages[:3]
    for i in recommendations:
        distance = gmaps.distance_matrix(location_from, i['address'], units='imperial')['rows'][0]['elements'][0]
        i['estimated_distance'] = distance['distance']['text']
        i['estimated_time'] = distance['duration']['text']

    return recommendations
