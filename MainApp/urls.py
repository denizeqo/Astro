from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('getReport', views.getReport, name='getReport'),
    path('translation', views.Translation, name='Translation')
]