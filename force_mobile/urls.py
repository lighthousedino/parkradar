from django.urls import path
from . import views

urlpatterns = [
    path('', views.force_mobile, name='force_mobile'),
]