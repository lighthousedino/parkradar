from django.shortcuts import render
# from django.http import HttpResponse
from datetime import datetime
import random

# import googlemaps
# gmaps = googlemaps.Client(key='AIzaSyBcqvNCEaFN8cgF2_f0038uKWBN038QKYE')



GARAGES = [
    {
        'name': 'Grand Arcade',
        'address': "St Andrew's St, Cambridge CB2 3BJ"
    },
    {
        'name': 'Grafton East',
        'address': "East Rd, Cambridge CB1 1PS"
    },
    {
        'name': 'Grafton West',
        'address': "Cambridge CB1 1HE"
    },
    {
        'name': 'Park Street',
        'address': "Park Street, Cambridge"
    },
    {
        'name': 'Queen Annes Terrace',
        'address': "Gonville Pl, Cambridge CB1 1ND"
    },
]


def recommend_garages(destination, day, time):
    recommendations = []

    garages = random.sample(GARAGES, 3)
    random.shuffle(garages)
    print(garages)
    return garages


def now(request):
    context = {
        'tab_active': 0
    }
    return render(request, 'parking/now.html', context)


def schedule(request):
    context = {
        'tab_active': 1
    }
    return render(request, 'parking/schedule.html', context)


def results(request):
    if request.method == 'POST':
        destination = request.POST['destination']
        day = request.POST['day']
        time = request.POST['time']

        if destination == '':
            context = {
                'no_location_error': True 
            }
            return render(request, 'parking/schedule.html', context)
        # if time == 'Now':
        #     time = datetime.now().strftime("%H:%M")
    
        
        garages = recommend_garages(destination, day, time)

        context = {
            'destination': destination,
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