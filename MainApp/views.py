from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from .chartUtility import *
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required

import json

from docx import Document
from docx.shared import Cm
from docx.shared import RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from io import BytesIO


from docxtpl import DocxTemplate
from docxtpl import InlineImage
from docx.shared import Cm

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from .charts.motherChart import MotherChart
from .charts.dailyChart import DailyChart
from .models import DailyCalendar, MonthlyCalendar


# Create your views here.


def Home(request):

    firstName = ""
    lastName = ""
    city = "Milan"
    country = "Italy"
    currentDate = datetime.now(ZoneInfo("Europe/Rome"))
    dateOfBirth = currentDate.strftime("%Y-%m-%d")
    timeOfBirth = currentDate.strftime("%H:%M")
    latitude = 45.4643
    longitude = 9.1895

    dailyChart = MotherChart(latitude, longitude, dateOfBirth, timeOfBirth, firstName, lastName, city, country)

    planets = dailyChart.planets
    fourAngles = dailyChart.fourAngles
    stars = dailyChart.stars
    chartData = dailyChart.userData

    return render(request, 'pages/home.html', {'asc':fourAngles[0]['position'],'currentDate':dateOfBirth, 'chartData':chartData, 'fourAngles': fourAngles, 'planets':planets, 'stars':stars, 'aspects':aspects})


def DailyChartPage(request):

    if request.method == 'POST':
        
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        dateOfBirth = request.POST.get('dateOfBirth')
        timeOfBirth = request.POST.get('timeOfBirth')
        country = request.POST.get('country')
        city = request.POST.get('city')
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        date = request.POST.get('date')
        time = request.POST.get('time')

        dailyChart = DailyChart(latitude, longitude, dateOfBirth, timeOfBirth, firstName, lastName, city, country, date, time)

        todayChartFourAngles = dailyChart.todayChartFourAngles

        birthChartUserData = dailyChart.birthChartUserData

        planets= dailyChart.combinePlanets

        stars = dailyChart.combineStars


        return JsonResponse({'asc':todayChartFourAngles[0]['position'], 'fourAngles': todayChartFourAngles, 'planets':planets, 'stars':stars, 'userData':birthChartUserData})
    return render(request, 'pages/dailyChart.html')


@staff_member_required
@require_POST
def DailyCalendarDescription(request):
    
    planetName = request.POST.get('planetName')
    description = request.POST.get('description')

    if 'Moon' in planetName:
        planet = DailyCalendar.objects.get(name='Moon')
    else:
        planet = DailyCalendar.objects.get(name=planetName)

    planet.description = description
    planet.save()

    return redirect('/dailyChart')


@staff_member_required
@require_POST
def MonthlyCalendarDescription(request):

    id = request.POST.get('id')
    description = request.POST.get('description')

    planet = MonthlyCalendar.objects.get(id=id)

    planet.description = description
    planet.save()

    return redirect('/dailyChart')
    


@staff_member_required
@require_POST
def MonthlyCalendarCreated(request):

    latesDate = MonthlyCalendar.objects.order_by('-timestamp')

    if len(latesDate) == 0:
        currentDate = datetime.now(ZoneInfo("Europe/Rome"))
    else:
        currentDate = latesDate[0].timestamp


    firstName = ""
    lastName = ""
    city = "Milan"
    country = "Italy"
    dateOfBirth = currentDate.strftime("%Y-%m-%d")
    timeOfBirth = currentDate.strftime("%H:%M")
    latitude = 45.4643
    longitude = 9.1895


    currenChart = MotherChart(latitude, longitude, dateOfBirth, timeOfBirth, firstName, lastName, city, country)
    planets = currenChart.planets

    currentHouses = {}

    for planet in planets:

        if 'Moon' in planet['name']:
            currentHouses['Moon'] = planet['house']['num']
        else:
             currentHouses[planet['name']] = planet['house']['num']


    for i in range(800):
        newDate =  currentDate + timedelta(hours=i)
        dateOfBirth = newDate.strftime("%Y-%m-%d")
        timeOfBirth = newDate.strftime("%H:%M")

        newChart = MotherChart(latitude, longitude, dateOfBirth, timeOfBirth, firstName, lastName, city, country)
        newPlanets = newChart.planets

        for planet in newPlanets:
            newHouse = planet['house']['num']

            if 'Moon' in planet['name']:
                if currentHouses['Moon'] != newHouse:
                    MonthlyCalendar.objects.create(name=planet['name'], 
                                                   houseNum=planet['house']['num'], 
                                                   houseSymbol=planet['house']['symbol'], 
                                                   position=newChart.degMin(planet['position']),
                                                   timestamp=newDate,
                                                   description='')
                    
                    currentHouses['Moon'] = planet['house']['num']

            else:
                if currentHouses[planet['name']] != newHouse:
                    MonthlyCalendar.objects.create(name=planet['name'], 
                                                   houseNum=planet['house']['num'], 
                                                   houseSymbol=planet['house']['symbol'], 
                                                   position=newChart.degMin(planet['position']),
                                                   timestamp=newDate,
                                                   description='')
                    
                    currentHouses[planet['name']] = planet['house']['num']


    #pList = ['Jupiter', 'Saturn', 'Uranus', 'Neptune', 'Pluto', 'Chiron']

    #for planet in newPlanets:

    #   if planet['name'] in pList:
    #        MonthlyCalendar.objects.create(name=planet['name'], 
     #                                           houseNum=planet['house']['num'], 
      #                                          houseSymbol=planet['house']['symbol'], 
       #                                         position=-1,
        #                                        timestamp=newDate + timedelta(hours=-100),
         #                                       description='')

    return redirect('/dailyChart')

    



def getReport(request):

    image = request.FILES["image"]
    userData = json.loads(request.POST['userData'])
    planetsData = json.loads(request.POST['planetsData'])
    starsData = json.loads(request.POST['starsData'])
    fourAnglesData = json.loads(request.POST['fourAnglesData'])
    aspectsData = json.loads(request.POST['aspectsData'])

    doc = DocxTemplate("test.docx")

    context = {
        "date": date.today(),
        "first_name": userData['First Name'],
        "last_name": userData['Last Name'],
        "country": userData['Country'],
        "city": userData['City'],
        "lat": userData['Latitude'],
        "lng": userData['Longitude'],
        "utc_time": userData['UTC Time'],
        "local_time": userData['Local Time'],
        "main_image": InlineImage(doc, image, width=Cm(17))
    }

    doc.render(context)
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)

    doc = Document(buffer)

    firstTable = doc.tables[0]

    index = 0
    for i in range(4):
        for j in range(3):
            
            talismanNum = userData['talisman'][index]['value']
            talismanNumColor = userData['talisman'][index]['color'][1:]

            talismanSup = userData['talisman'][index]['sup']
            talismanSupColor = userData['talisman'][index]['supColor'][1:]

            cell = firstTable.cell(i, j + 3)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run1 = p.add_run(str(talismanNum))
            run1.font.color.rgb = RGBColor.from_string(talismanNumColor)
            run1.font.name = 'Poppins'

            if talismanSup != '':
                run2 = p.add_run(str(talismanSup))
                run2.font.color.rgb = RGBColor.from_string(talismanSupColor)
                run2.font.name = 'Poppins'

            index += 1
    
    creat_asc_table(doc, fourAnglesData)
    create_planet_table(doc, planetsData)
    creat_stars_table(doc, starsData)
    creat_aspects_table(doc, aspectsData)
    
    
            
    doc.save(buffer)
    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename="report.docx",
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )







def Weel(request):

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
        print(len(aspects))
        userData = getUserData(chart, latitude, longitude, dateOfBirth, timeOfBirth, firstName, lastName, city, country)

        
        return JsonResponse({'userData':userData, 'fourAngles': fourAngles, 'planets':planets, 'stars':stars, 'staticChartSymbols': staticChartSybols, 'dynamicChartSymbols':dynamicChartSymbols, 'aspects':aspects})

    return render(request, 'pages/wheelOfDestiny.html')



def AboutUs(request):

    return render(request, 'pages/aboutUs.html')


def AstroShop(request):

    return render(request, 'pages/astroShop.html')

def EverythingAbout(request):


    firstName = ""
    lastName = ""
    city = "Milan"
    country = "Italy"
    currentDate = datetime.now(ZoneInfo("Europe/Rome"))
    dateOfBirth = currentDate.strftime("%Y-%m-%d")
    timeOfBirth = currentDate.strftime("%H:%M")
    latitude = 45.4643
    longitude = 9.1895

    dailyChart = DailyChart(latitude, longitude, dateOfBirth, timeOfBirth, firstName, lastName, city, country)

    planets = dailyChart.planets
    fourAngles = dailyChart.fourAngles
    stars = dailyChart.stars
    aspects = dailyChart.aspects
    chartData = dailyChart.userData
    starsForPlanet = dailyChart.getStarsForPlanet()
    monthlyCalendar = dailyChart.getMonthlyCalendar()


    return render(request, 'pages/everythingAboutAstro.html', {'asc':fourAngles[0]['position'],'currentDate':dateOfBirth, 'chartData':chartData, 'fourAngles': fourAngles, 'planets':planets, 'stars':stars, 'aspects':aspects, 'starsForPlanet':starsForPlanet, 'monthlyCalendar':monthlyCalendar})


def prBirthChart(request):

    return render(request, 'pages/products/birthChart.html')


def prLunar(request):

    return render(request, 'pages/products/lunar.html')


def prForecast(request):

    return render(request, 'pages/products/forecast.html')



def prEvolution(request):

    return render(request, 'pages/products/evolution.html')



def prAncientWisdom(request):

    return render(request, 'pages/products/ancientWisdom.html')




def prRelationships(request):

    return render(request, 'pages/products/relationships.html')



def prAstrography(request):

    return render(request, 'pages/products/astrography.html')



def prSoul(request):

    return render(request, 'pages/products/soul.html')



def prMagnetism(request):

    return render(request, 'pages/products/magnetism.html')



def prInnerWorld(request):

    return render(request, 'pages/products/innerWorld.html')



def prEssentialOils(request):

    return render(request, 'pages/products/essentialOils.html')




def prStars(request):

    return render(request, 'pages/products/stars.html')