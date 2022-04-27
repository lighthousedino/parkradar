from django.shortcuts import render

# Create your views here.
def landing(request):
    context = {}
    return render(request, 'parking/force-mobile.html', context)