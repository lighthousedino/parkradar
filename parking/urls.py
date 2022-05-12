from django.urls import path
from . import views

urlpatterns = [
    path('', views.now, name='now'),
    path('plan-ahead/', views.ahead, name='ahead'),
    path('results/', views.results, name='results'),
    path('settings/', views.settings, name='settings'),
]