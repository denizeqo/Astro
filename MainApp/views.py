from django.shortcuts import render
from django.http import JsonResponse
from .chartUtility import *
import json

# Create your views here.
def Home(request):

    if request.method == 'POST':

        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        dateOfBirth = request.POST.get('dateOfBirth')
        timeOfBirth = request.POST.get('timeOfBirth')
        country = request.POST.get('country')
        city = request.POST.get('city')
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))

        chart = createChart(latitude, longitude, dateOfBirth, timeOfBirth)      

        planets = getPlanets(chart)
        fourAngles = getFourAngles(chart)
        stars = getStars(planets, fourAngles)

        staticChartSybols = getChartSymbols(0)
        dynamicChartSymbols = getChartSymbols(fourAngles[0]['position'])

        aspects = get_all_aspects(chart)

        userData = getUserData(chart, latitude, longitude, dateOfBirth, timeOfBirth, firstName, lastName, city, country)

        
        return JsonResponse({'userData':userData, 'fourAngles': fourAngles, 'planets':planets, 'stars':stars, 'staticChartSymbols': staticChartSybols, 'dynamicChartSymbols':dynamicChartSymbols})

    return render(request, 'pages/home.html')