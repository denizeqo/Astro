from django.shortcuts import render
from django.http import JsonResponse
from .chartUtility import *
import json

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

        stars = {
            'algenib': chart.getFixedStar(const.STAR_ALGENIB).lon,
            'alpheratz': chart.getFixedStar(const.STAR_ALPHERATZ).lon,
            'algol': chart.getFixedStar(const.STAR_ALGOL).lon,
            'alcyone': chart.getFixedStar(const.STAR_ALCYONE).lon,
            'aldebaran': chart.getFixedStar(const.STAR_ALDEBARAN).lon,
            'rigel': chart.getFixedStar(const.STAR_RIGEL).lon,
            'capella': chart.getFixedStar(const.STAR_CAPELLA).lon,
            'betelgeuse': chart.getFixedStar(const.STAR_BETELGEUSE).lon,
            'sirius': chart.getFixedStar(const.STAR_SIRIUS).lon,
            'canopus': chart.getFixedStar(const.STAR_CANOPUS).lon,
            'castor': chart.getFixedStar(const.STAR_CASTOR).lon,
            'pollux': chart.getFixedStar(const.STAR_POLLUX).lon,
            'procyon': chart.getFixedStar(const.STAR_PROCYON).lon,
            'asellus_borealis': chart.getFixedStar(const.STAR_ASELLUS_BOREALIS).lon,
            'asellus_australis': chart.getFixedStar(const.STAR_ASELLUS_AUSTRALIS).lon,
            'alphard': chart.getFixedStar(const.STAR_ALPHARD).lon,
            'regulus': chart.getFixedStar(const.STAR_REGULUS).lon,
            'denebola': chart.getFixedStar(const.STAR_DENEBOLA).lon,
            'algorab': chart.getFixedStar(const.STAR_ALGORAB).lon,
            'spica': chart.getFixedStar(const.STAR_SPICA).lon,
            'arcturus': chart.getFixedStar(const.STAR_ARCTURUS).lon,
            'alphecca': chart.getFixedStar(const.STAR_ALPHECCA).lon,
            'zuben_elgenubi': chart.getFixedStar(const.STAR_ZUBEN_ELGENUBI).lon,
            'zuben_elschemali': chart.getFixedStar(const.STAR_ZUBEN_ELSCHEMALI).lon,
            'unukalhai': chart.getFixedStar(const.STAR_UNUKALHAI).lon,
            'agena': chart.getFixedStar(const.STAR_AGENA).lon,
            'rigel_kentaurus': chart.getFixedStar(const.STAR_RIGEL_CENTAURUS).lon,
            'antares': chart.getFixedStar(const.STAR_ANTARES).lon,
            'lesath': chart.getFixedStar(const.STAR_LESATH).lon,
            'vega': chart.getFixedStar(const.STAR_VEGA).lon,
            'altair': chart.getFixedStar(const.STAR_ALTAIR).lon,
            'deneb_algedi': chart.getFixedStar(const.STAR_DENEB_ALGEDI).lon,
            'fomalhaut': chart.getFixedStar(const.STAR_FOMALHAUT).lon,
            'deneb': chart.getFixedStar(const.STAR_DENEB_ADIGE).lon,
            'achernar': chart.getFixedStar(const.STAR_ACHERNAR).lon,
        }

        

        planets = {
            'sun': chart.get(const.SUN).lon,
            'moon': chart.get(const.MOON).lon,
            'northMoon': chart.get(const.NORTH_NODE).lon,
            'southMoon': chart.get(const.SOUTH_NODE).lon,
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

        asc = {
            'asc':asc.lon,
            'mc':mc.lon,
            'ic':ic.lon,
            'dsc':dsc.lon
        }
        
        stars = getStarsData(planets, asc)


        return JsonResponse({'asc':asc, 'planets':planets, 'stars':stars})

    return render(request, 'pages/home.html')