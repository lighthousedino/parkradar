from django.urls import path
from . import views

urlpatterns = [
    path('', views.now, name='now'),
    path('schedule/', views.schedule, name='schedule'),
    path('results/', views.results, name='results'),
    path('settings/', views.settings, name='settings'),
]