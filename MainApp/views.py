from django.shortcuts import render
from django.http import JsonResponse
from .chartUtility import *

from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
import swisseph as swe

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

        objects = [
                    const.SUN,
                    const.MOON,
                    const.MERCURY,
                    const.VENUS,
                    const.MARS,
                    const.JUPITER,
                    const.SATURN,
                    const.URANUS,
                    const.NEPTUNE,
                    const.PLUTO,
                    const.CHIRON,
                    const.NORTH_NODE,
                    const.SOUTH_NODE,
                ]
        
        swe.set_ephe_path(r"C:\\Users\\User\\OneDrive\\Desktop\\Dei\\Project\\Eureka\\Astro\\Astro\\sweph\\ephe")

        date = Datetime(dateOfBirth, timeOfBirth, '+00:00')
        pos = GeoPos(lat, lon)
        chart = Chart(date, pos, IDs=objects)

        asc = chart.get(const.ASC)
        mc = chart.get(const.MC)
        ic = chart.get(const.IC)
        dsc = chart.get(const.DESC)
        
        sun = chart.get(const.SUN)

        for obj in chart.objects:
            print(obj)

        planets = {
            'sun': chart.get(const.SUN).lon,
            'moon': chart.get(const.MOON).lon,
            'mercury': chart.get(const.MERCURY).lon,
            'venus': chart.get(const.VENUS).lon,
            'mars': chart.get(const.MARS).lon,
            'jupiter':chart.get(const.JUPITER).lon,
            'saturn': chart.get(const.SATURN).lon,
            'uranus': chart.getObject(const.URANUS).lon,
            'neptune': chart.get(const.NEPTUNE).lon,
            'pluto': chart.get(const.PLUTO).lon,
            'chiron': chart.get(const.CHIRON).lon
        }

        return JsonResponse({'asc':asc.lon, 'mc':mc.lon, 'ic':ic.lon, 'dsc':dsc.lon, 'planets':planets})


    return render(request, 'pages/home.html')