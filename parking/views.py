from django.shortcuts import render
from datetime import datetime
import calendar
import random
from db.queries import Garages, DemoLocation
import googlemaps
import numpy as np

gmaps = googlemaps.Client(key='AIzaSyBcqvNCEaFN8cgF2_f0038uKWBN038QKYE')


def recommend_garage_now(location_from):
    '''
    Return the cloest garage whose current occupancy is less than 90%
    '''
    all_garages = Garages.get()
    rank_distance = []

    for i in all_garages:
        distance = gmaps.distance_matrix(location_from, i[1]['address'], units='imperial')['rows'][0]['elements'][0]
        rank_distance.append(distance['distance']['value'])
    
    sorted_indices = np.argsort(rank_distance)

    for i in range(len(sorted_indices)):
        recommendation = all_garages[sorted_indices[i]][1]
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
    all_garages = Garages.get()

    random_samples = random.sample(all_garages, 3)
    random.shuffle(random_samples)

    for i in random_samples:
        distance = gmaps.distance_matrix(location_from, i[1]['address'], units='imperial')['rows'][0]['elements'][0]
        i[1]['estimated_distance'] = distance['distance']['text']
        i[1]['estimated_time'] = distance['duration']['text']
        i[1]['percentage_occupied'] = round(i[1]['current_occupancy'] / i[1]['max_occupancy'] * 100)
        
        recommendations.append(i[1])

    return recommendations


def now(request):
    location_from = DemoLocation.get()
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
    location_from = DemoLocation.get()
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
