from django.shortcuts import render
from django.http import JsonResponse
from .chartUtility import *

from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

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

        lat, lon = getLonLat(latitude, longitude)
        dateOfBirth, timeOfBirth = getUTCDateTime(dateOfBirth, timeOfBirth, latitude, longitude)

        date = Datetime(dateOfBirth, timeOfBirth, '+00:00')
        pos = GeoPos(lat, lon)
        chart = Chart(date, pos)

        asc = chart.get(const.ASC)
        mc = chart.get(const.MC)
        ic = chart.get(const.IC)
        dsc = chart.get(const.DESC)


        sun = chart.get(const.SUN)
        print(ic.lon)
        print(mc.lon)
        print(asc.lon)
        print(dsc.lon)

        return JsonResponse({'asc':asc.lon, 'mc':mc.lon, 'ic':ic.lon, 'dsc':dsc.lon})


    return render(request, 'pages/home.html')