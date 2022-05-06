from django.shortcuts import render
# from django.http import HttpResponse
from datetime import datetime
import calendar
import random

# import googlemaps
# gmaps = googlemaps.Client(key='AIzaSyBcqvNCEaFN8cgF2_f0038uKWBN038QKYE')


DEFAULT_LOCATION_FROM = '2044 E Monterey Way, Phoenix'
# DEFAULT_LOCATION_FROM = '2044 E Monterey Way, Phoenix, AZ 85016'

REGISTERED_GARAGES = [
    {
        'name': 'Louisa Kellam Center',
        'address': "Louisa Kellam Center Visitor Parking, West Meeker Boulevard, Sun City West"
    },
    {
        'name': 'Encanto Park North',
        'address': "Encanto Park North Parking Lot, North 15th Avenue, Phoenix"
    },
    {
        'name': 'Luhrs City Center Parking',
        'address': "Luhrs City Center Parking - ParkChirp, South 1st Avenue, Phoenix"
    },
    {
        'name': 'Phoenix Convention Center',
        'address': "Phoenix Convention Center - Regency Garage, North 2nd Street, Phoenix"
    },
    {
        'name': 'Jefferson Street Garage',
        'address': "Jefferson Street Garage, East Jefferson Street, Phoenix"
    },
    {
        'name': 'Civic Center Library',
        'address': "Civic Center Library Parking Garage, North Drinkwater Boulevard, Scottsdale"
    },
    {
        'name': 'East Lake View Drive',
        'address': "East Lake View Drive Parking, East Lake View Drive, Tempe"
    },
    {
        'name': 'Chase Parking Garage',
        'address': "Chase Parking Garage Entrance, South Ash Avenue, Tempe"
    },
]


def recommend_garages(destination, day, time):
    recommendations = []

    garages = random.sample(REGISTERED_GARAGES, 3)
    random.shuffle(garages)
    return garages


def now(request):
    day = calendar.day_name[datetime.today().weekday()]
    time = datetime.now().strftime("%H:%M")
    garages = recommend_garages(DEFAULT_LOCATION_FROM, day, time)
    context = {
        'location_from': DEFAULT_LOCATION_FROM,
        'day': day,
        'time': time,
        # 'garages': garages,
        'first_garage': garages[0],
        'tab_active': 0
    }
    return render(request, 'parking/now.html', context)


def schedule(request):
    context = {
        'location_from': DEFAULT_LOCATION_FROM,
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