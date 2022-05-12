from django.shortcuts import render
from datetime import datetime
import calendar
from . import recommend


DEMO_LOCATION = '2044 E Monterey Way, Phoenix'


def now(request):
    location_from = DEMO_LOCATION
    day = calendar.day_name[datetime.today().weekday()]
    time = datetime.now().strftime("%H:%M")
    recommendation = recommend.now(location_from, day, time)
    context = {
        'location_from': location_from,
        'day': day,
        'time': time,
        'first_garage': recommendation,
        'tab_active': 0
    }
    return render(request, 'parking/now.html', context)


def ahead(request):
    location_from = DEMO_LOCATION
    context = {
        'location_from': location_from,
        'tab_active': 1
    }
    return render(request, 'parking/ahead.html', context)


def results(request):
    if request.method == 'POST':
        location_from = request.POST['location_from']
        day = request.POST['day']
        time = f'{request.POST["hour"]}:{request.POST["minute"]}'

        if location_from == '':
            location_from = DEMO_LOCATION
        
        recommendations = recommend.ahead(location_from, day, time)
        
        context = {
            'location_from': location_from,
            'day': day,
            'time': time,
            'garages': recommendations,
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
