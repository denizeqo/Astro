from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home, name='Home'),
    path('getReport', views.getReport, name='getReport'),
    path('weel', views.Weel, name='weel'),
    path('dailyChart', views.DailyChartPage),
    path('aboutUs', views.AboutUs, name='aboutUs'),
    path('registerDescription', views.DailyCalendarDescription, name='registerDescription'),
    path('monthlyCalendarCreated', views.MonthlyCalendarCreated),
    path('registerMonthlyCalendarDescription', views.MonthlyCalendarDescription),
    path('astroShop', views.AstroShop, name='astroShop'),
    path('everythingAbout', views.EverythingAbout, name='everythingAbout'),

]