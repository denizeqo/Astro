from django.shortcuts import render
from django.http import JsonResponse

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

        latDeg = int(latitude)
        latMin =int((latitude - latDeg) * 60)

        latStr = str(latDeg) + 'n' + str(latMin)

        lonDeg = int(longitude)
        lonMin = int((longitude - lonDeg) * 60)

        lonStr = str(lonDeg) + 'e' + str(lonMin)





        dateOfBirth = '/'.join(dateOfBirth.split('-'))

        date = Datetime(dateOfBirth, timeOfBirth, '+00:00')
        pos = GeoPos(latStr, lonStr)
        chart = Chart(date, pos)

        asc = chart.get(const.ASC)
        sun = chart.get(const.SUN)
        print(sun.lon)
        print(asc.lon)

        print(dateOfBirth)
        print(timeOfBirth)
        print(latStr)
        print(lonStr)

        return JsonResponse({'asc':asc.lon})


    return render(request, 'pages/home.html')