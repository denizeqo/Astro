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
    path('birthChart', views.prBirthChart, name='birthChart'),
    path('lunar', views.prLunar, name='lunar'),
    path('evolution', views.prEvolution, name='evolution'),
    path('ancientwisdom', views.prAncientWisdom, name='ancientwisdom'),
    path('relationships', views.prRelationships, name='relationships'),
    path('astrography', views.prAstrography, name='astrography'),
    path('soul', views.prSoul, name='soul'),
    path('magnetism', views.prMagnetism, name='magnetism'),
    path('innerWorld', views.prInnerWorld, name='innerWorld'),
    path('essentialOils', views.prEssentialOils, name='essentialOils'),
    path('stars', views.prStars, name='stars'),
    path('forecast', views.prForecast, name='forecast'),
    path('create-admin/', views.create_admin, name='create_admin'),

]