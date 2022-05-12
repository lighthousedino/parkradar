import numpy as np
import googlemaps
from garages import registered_garages


REGISTERED_GARAGES = registered_garages.REGISTERED_GARAGES
gmaps = googlemaps.Client(key='AIzaSyBcqvNCEaFN8cgF2_f0038uKWBN038QKYE')


def now(location_from, day, time):
    '''
    Return the cloest garage whose current occupancy is less than 90%
    '''
    garages = np.array(REGISTERED_GARAGES)
    rank_distance = []
    for i in garages:
        distance = gmaps.distance_matrix(location_from, i['address'], units='imperial')['rows'][0]['elements'][0]
        rank_distance.append(distance['distance']['value'])
    sorted_indices = np.argsort(rank_distance)

    for i in range(len(sorted_indices)):
        recommendation = garages[sorted_indices[i]]
        distance = gmaps.distance_matrix(location_from, recommendation['address'], units='imperial')['rows'][0]['elements'][0]
        recommendation['estimated_distance'] = distance['distance']['text']
        recommendation['estimated_time'] = distance['duration']['text']
        recommendation['percentage_occupied'] = round(recommendation['current_occupancy'] / recommendation['max_occupancy'] * 100)

        if recommendation['percentage_occupied'] >= 90 and i != len(sorted_indices):
            continue
        else:
            break

    return recommendation


def ahead(location_from, day, time):
    garages = np.array(REGISTERED_GARAGES)
    rank_distance = []
    for i in garages:
        distance = gmaps.distance_matrix(location_from, i['address'], units='imperial')['rows'][0]['elements'][0]
        rank_distance.append(distance['distance']['value'])
    sorted_indices = np.argsort(rank_distance)
    garages = garages[sorted_indices] # sorted list of all garages; closest first

    recommendations = garages[:3]

    for i in recommendations:
        distance = gmaps.distance_matrix(location_from, i['address'], units='imperial')['rows'][0]['elements'][0]
        i['estimated_distance'] = distance['distance']['text']
        i['estimated_time'] = distance['duration']['text']
        i['percentage_occupied'] = round(i['current_occupancy'] / i['max_occupancy'] * 100)
        
    return recommendations
