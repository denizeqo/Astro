from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from .chartUtility import *
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

from datetime import date, datetime



# Create your views here.

def Home(request):
    firstName = ""
    lastName = ""
    city = ""
    country = ""
    currentDate = datetime.now()
    dateOfBirth = currentDate.strftime("%Y-%m-%d")
    timeOfBirth = currentDate.strftime("%H:%M")
    latitude = 41.1197
    longitude = 20.8022

    chart = createChart(latitude, longitude, dateOfBirth, timeOfBirth)      

    planets = getPlanets(chart)
    fourAngles = getFourAngles(chart)
    stars = getStars(planets, fourAngles)

    staticChartSybols = getChartSymbols(0)
    dynamicChartSymbols = getChartSymbols(fourAngles[0]['position'])

    aspects = get_all_aspects(chart)
    print(len(aspects))
    userData = getUserData(chart, latitude, longitude, dateOfBirth, timeOfBirth, firstName, lastName, city, country)

    with open("C:\\Users\\User\\OneDrive\\Desktop\\Dei\\Project\\Eureka\\Astro\\Astro\\sweph\\ephe\\planetNum.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    


    planetStars = {}
    for i in planets:
        planetNum = i['num']['value']
        planetSup = i['num']['sup']
        planetName = i['name']

        for j in stars:

            if j['num']['value'] == planetNum and j['num']['sup'] == planetSup:
                
                if planetStars.get(planetName, -1) == -1:
                    planetStars[planetName] = [j['name']]
                else:
                    planetStars[planetName].append(j['name'])



    for i in planets:

        name = i['name']
        planetNums = data.get(name, False)

        if i['num']['value'] <= 10:
            i['num']['value'] = ''
            i['num']['sup'] = ''
            i['num']['color'] = '#ffffff'
        elif planetNums:
            if i['num']['value'] in planetNums:
                pass
            else:
                i['num']['value'] = ''
                i['num']['sup'] = ''
                i['num']['color'] = '#ffffff'
        else:
            i['num']['value'] = ''
            i['num']['sup'] = ''
            i['num']['color'] = '#ffffff'
    

    for i in stars:
        i['num']['value'] = ''
        i['num']['sup'] = ''
        i['num']['color'] = '#ffffff'


    fourAngles[2]['num'] = {'value':'', 'sup':'', 'color':'#ffffff', 'supColor':'#ffffff'}
    fourAngles[3]['num'] = {'value':'', 'sup':'', 'color':'#ffffff', 'supColor':'#ffffff'}
    

    return render(request, 'pages/home.html', {'asc':fourAngles[0]['position'], 'userData':userData, 'fourAngles': fourAngles, 'planets':planets, 'stars':stars, 'staticChartSymbols': staticChartSybols, 'dynamicChartSymbols':dynamicChartSymbols, 'aspects':aspects, 'planetStars':planetStars})


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