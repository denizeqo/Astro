from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse, FileResponse
from .chartUtility import *
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required

import json
from pathlib import Path

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
from .models import DailyCalendar, MonthlyCalendar, Transit


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
    aspects = dailyChart.aspects
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
        birthChartUserData = dailyChart.todayChartUserData
        planets= dailyChart.combinePlanets
        stars = dailyChart.combineStars
        todayPlanets = dailyChart.todayChartPlanets

        with open(Path(MotherChart.ephePath) / "astro_planet_translations_complete.json","r",encoding="utf-8") as file:
            planetsTransit = json.load(file)

        rr = []
        for p in todayPlanets:
            pName = p['name']
            pHouseNum = p['house']['num']

            if 'Moon' in pName:
                pName = 'moon'

            for i in planetsTransit['planet_houses']:

                if i['planet'] == pName.lower() and i['house'] == pHouseNum:
                    translation = i['translations'].get(request.LANGUAGE_CODE) or i['translations'].get('en', {})
                    rr.append({'planet':p['name'],
                               'planetColor':p['color'],
                               'planetPosition':p['position'],
                               'planetHouse':p['house'],
                               #'title':i['translations'][request.LANGUAGE_CODE]['title'],
                               'title':dailyChart.getTransitTitle(p)['titleHtml'],
                               'description':translation.get('description', ''),
                               'warning':translation.get('warning', '')})
                    

        with open(Path(MotherChart.ephePath) / "astro_archetypes_multilingual.json","r",encoding="utf-8") as file:
            arketipDescription = json.load(file)

        ss = dailyChart.getStarsForPlanet()
        for p in ss:
            
            if p['num']['sup'] == '':
                entryB = arketipDescription['B'].get(str(p['num']['value'])) or {}
                p['description'] = entryB.get(request.LANGUAGE_CODE) or entryB.get('en', '')
                p['subtitle'] = p['num']['arketip']
                p['title'] = dailyChart.getPlanetTitle(p)['titleHtml']
            else:
                entryA = arketipDescription['A'].get(str(p['num']['value'])) or {}
                p['description'] = entryA.get(request.LANGUAGE_CODE) or entryA.get('en', '')
                p['subtitle'] = p['num']['arketip']
                p['title'] = dailyChart.getPlanetTitle(p)['titleHtml']
                
        
        with open(Path(MotherChart.ephePath) / "aspects.json","r",encoding="utf-8") as file:
            aspectsDescription = json.load(file)

        aspectList = []
        for aspect in dailyChart.todayChart.aspects:

            des = aspectsDescription.get(aspect['active'],{}).get(aspect['passive'],{}).get(aspect['deg'],{}).get(request.LANGUAGE_CODE,None)

            if des:
                title = f"<span style=\"color: {aspect['activeColor']}; font-family: 'Poppins', sans-serif; text-align: center;\">{aspect['active']}</span> {aspect['type']} <span style=\"color: {aspect['passiveColor']}; font-family: 'Poppins', sans-serif; text-align: center;\">{aspect['passive']}</span> — {aspect['orb']}° {aspect['movement']}"
                aspectList.append({'description':des, 'title':title})



        return JsonResponse({'asc':todayChartFourAngles[0]['position'], 'fourAngles': todayChartFourAngles, 'planets':planets, 'stars':stars, 'userData':birthChartUserData, 'transit':rr, 'arketipet':ss, 'aspects':aspectList})
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
    


def MonthlyCalendarCreated(request):

    latesDate = Transit.objects.order_by('-endAt')

    if len(latesDate) == 0:
        currentDate = datetime.now(ZoneInfo("Europe/Rome"))
    else:
        currentDate = latesDate[0].endAt


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
            currentHouses['Moon'] = {'startAt':None, 'houseNum':planet['house']['num'], 'R':False}
        else:
             currentHouses[planet['name']] = {'startAt':None, 'houseNum':planet['house']['num'], 'R':False}


    h = 1
    for i in range(800):
        newDate =  currentDate + timedelta(hours=h)
        dateOfBirth = newDate.strftime("%Y-%m-%d")
        timeOfBirth = newDate.strftime("%H:%M")

        newChart = MotherChart(latitude, longitude, dateOfBirth, timeOfBirth, firstName, lastName, city, country)
        newPlanets = newChart.planets

        for planet in newPlanets:
            newHouse = planet['house']['num']
            
            


            if 'Moon' in planet['name']:
                if planet['movement'] == 'Retrograde':
                    currentHouses['Moon']['R'] = True

                if currentHouses['Moon']['houseNum'] != newHouse:
                    Transit.objects.create(planetName=planet['name'], 
                                                   houseNum=currentHouses['Moon']['houseNum'], 
                                                   endAt=newDate,
                                                   startAt=currentHouses['Moon']['startAt'],
                                                   retrograde=currentHouses['Moon']['R'])
                    
                    currentHouses['Moon']['houseNum'] = planet['house']['num']
                    currentHouses['Moon']['startAt'] = newDate
                    currentHouses['Moon']['R'] = False

            else:
                if planet['movement'] == 'Retrograde':
                    currentHouses[planet['name']]['R'] = True

                if currentHouses[planet['name']]['houseNum'] != newHouse:
                    Transit.objects.create(planetName=planet['name'], 
                                                   houseNum=currentHouses[planet['name']]['houseNum'],  
                                                   endAt=newDate,
                                                   startAt=currentHouses[planet['name']]['startAt'],
                                                   retrograde=currentHouses[planet['name']]['R'])
                    
                    currentHouses[planet['name']]['houseNum'] = planet['house']['num']
                    currentHouses[planet['name']]['startAt'] = newDate
                    currentHouses[planet['name']]['R'] = False

        h += 5

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

    dailyChart = DailyChart(latitude, longitude, dateOfBirth, timeOfBirth, firstName, lastName, city, country, dateOfBirth, timeOfBirth)

    planets = dailyChart.birthChartPlanets
    fourAngles = dailyChart.birthChartFourAngles
    stars = dailyChart.birthChartStars
    aspects = dailyChart.birthChart.aspects
    chartData = dailyChart.birthChartUserData
    starsForPlanet = dailyChart.getStarsForPlanet()


    return render(request, 'pages/everythingAboutAstro.html', {'asc':fourAngles[0]['position'],'currentDate':dateOfBirth, 'chartData':chartData, 'fourAngles': fourAngles, 'planets':planets, 'stars':stars, 'aspects':aspects, 'starsForPlanet':starsForPlanet})


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


def create_admin(request):
    from django.contrib.auth.models import User
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@astro.com', 'ChangeMe123!')
        return HttpResponse('Superuser created: username=admin, password=ChangeMe123!')
    return HttpResponse('Superuser already exists')