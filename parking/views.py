from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime
import random


GARAGES = [
    'Grand Arcade',
    'Grafton East',
    'Grafton West',
    'Park Street',
    'Queen Annes Terrace',
]


# Create your views here.

def home(request):
    context = {}
    return render(request, 'parking/home.html', context)

def results(request):
    if request.method == 'POST':
        destination = request.POST['destination']
        time = request.POST['time']
        if time == 'Now':
            time = datetime.now().strftime("%H:%M")
        

        selected_garages = random.sample(GARAGES, 3)
        random.shuffle(selected_garages)
        # print(selected_garages)

        # context
        input = {
                'destination': destination,
                'time': time
        }
        output = selected_garages

        context = {
            'input': input,
            'output': output,
        }
        return render(request, 'parking/results.html', context)
    else:
        pass