from django.shortcuts import render
from datetime import datetime
import calendar
import random
from db.queries import Garages, DemoLocation


def recommend_garages(destination, day, time):
    recommendations = []
    all_garages = Garages.get()

    random_samples = random.sample(all_garages, 3)
    random.shuffle(random_samples)

    for i in random_samples:
        recommendations.append(i[1])

    return recommendations


def now(request):
    location_from = DemoLocation.get()
    day = calendar.day_name[datetime.today().weekday()]
    time = datetime.now().strftime("%H:%M")
    garages = recommend_garages(location_from, day, time)
    context = {
        'location_from': location_from,
        'day': day,
        'time': time,
        # 'garages': garages,
        'first_garage': garages[0],
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
