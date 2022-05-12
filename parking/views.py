from django.shortcuts import render
from datetime import datetime
import calendar
import random
import googlemaps
import numpy as np
from garages import registered_garages

REGISTERED_GARAGES = registered_garages.REGISTERED_GARAGES
DEMO_LOCATION = '2044 E Monterey Way, Phoenix'

gmaps = googlemaps.Client(key='AIzaSyBcqvNCEaFN8cgF2_f0038uKWBN038QKYE')


def recommend_garage_now(location_from):
    '''
    Return the cloest garage whose current occupancy is less than 90%
    '''
    all_garages = REGISTERED_GARAGES.copy()
    rank_distance = []

    for i in all_garages:
        distance = gmaps.distance_matrix(location_from, i['address'], units='imperial')['rows'][0]['elements'][0]
        rank_distance.append(distance['distance']['value'])
    
    sorted_indices = np.argsort(rank_distance)

    for i in range(len(sorted_indices)):
        recommendation = all_garages[sorted_indices[i]]
        distance = gmaps.distance_matrix(location_from, recommendation['address'], units='imperial')['rows'][0]['elements'][0]
        recommendation['estimated_distance'] = distance['distance']['text']
        recommendation['estimated_time'] = distance['duration']['text']
        recommendation['percentage_occupied'] = round(recommendation['current_occupancy'] / recommendation['max_occupancy'] * 100)

        if recommendation['percentage_occupied'] >= 90 and i != len(sorted_indices):
            continue
        else:
            break

    return recommendation


def recommend_garages(location_from, day, time):
    recommendations = []
    all_garages = REGISTERED_GARAGES.copy()

    random_samples = random.sample(all_garages, 3)
    random.shuffle(random_samples)

    for i in random_samples:
        distance = gmaps.distance_matrix(location_from, i['address'], units='imperial')['rows'][0]['elements'][0]
        i['estimated_distance'] = distance['distance']['text']
        i['estimated_time'] = distance['duration']['text']
        i['percentage_occupied'] = round(i['current_occupancy'] / i['max_occupancy'] * 100)
        
        recommendations.append(i)

    return recommendations


def now(request):
    location_from = DEMO_LOCATION
    day = calendar.day_name[datetime.today().weekday()]
    time = datetime.now().strftime("%H:%M")
    recommendation = recommend_garage_now(location_from)
    context = {
        'location_from': location_from,
        'day': day,
        'time': time,
        'first_garage': recommendation,
        'tab_active': 0
    }
    return render(request, 'parking/now.html', context)


def schedule(request):
    location_from = DEMO_LOCATION
    context = {
        'location_from': location_from,
        'tab_active': 1
    }
    return render(request, 'parking/schedule.html', context)


def results(request):
    if request.method == 'POST':
        location_from = request.POST['location_from']
        day = request.POST['day']
        time = request.POST['time']

        if location_from == '':
            context = {
                'no_location_error': True 
            }
            return render(request, 'parking/schedule.html', context)
        # if time == 'Now':
        #     time = datetime.now().strftime("%H:%M")
    
        
        garages = recommend_garages(location_from, day, time)

        context = {
            'location_from': location_from,
            'day': day,
            'time': time,
            'garages': garages,
            'tab_active': 1
        }
        return render(request, 'parking/results.html', context)

    else:
        return render(request, 'parking/results.html')


def settings(request):
    context = {
        'tab_active': 2
    }
    return render(request, 'parking/settings.html', context)
