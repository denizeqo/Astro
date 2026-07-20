from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('getReport', views.getReport, name='getReport'),
    path('weel', views.Weel, name='weel'),
    path('aboutUs', views.AboutUs, name='aboutUs'),
    path('registerDescription', views.DailyCalendarDescription, name='registerDescription')
]