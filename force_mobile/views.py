from django.shortcuts import render

# Create your views here.
def force_mobile(request):
    context = {}
    return render(request, 'force_mobile/force-mobile.html', context)