from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from .chartUtility import *
import json

from docx import Document
from docx.shared import Cm
from docx.shared import RGBColor
from io import BytesIO

from deep_translator import GoogleTranslator

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
        print(len(aspects))
        userData = getUserData(chart, latitude, longitude, dateOfBirth, timeOfBirth, firstName, lastName, city, country)

        
        return JsonResponse({'userData':userData, 'fourAngles': fourAngles, 'planets':planets, 'stars':stars, 'staticChartSymbols': staticChartSybols, 'dynamicChartSymbols':dynamicChartSymbols, 'aspects':aspects})

    return render(request, 'pages/home.html')


def getReport(request):

    image = request.FILES["image"]
    userData = json.loads(request.POST['userData'])

    document = Document()

    section = document.sections[0]

    style = document.styles['Normal']
    font = style.font
    font.name = 'Arial'

    section.top_margin = Cm(1.27)
    section.bottom_margin = Cm(1.27)
    section.left_margin = Cm(1.27)
    section.right_margin = Cm(1.27)

    document.add_heading("Report", level=1)
    document.add_picture(image, width=Cm(19))

    #document.add_heading('User Data', level=2)

    table = document.add_table(rows=0, cols=3)

    addTableRows(table, userData)

    p = document.add_paragraph('')
    p.add_run('Chart System: Astro-Numerology Egizio').bold =True

    buffer = BytesIO()
    document.save(buffer)
    buffer.seek(0)

    return FileResponse(
        buffer,
        as_attachment=True,
        filename="report.docx",
        content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )



def Translation(request):

    if request.method == 'POST':
        sourceLang = request.POST.get('sourceLang')
        targetLang = request.POST.get('targetLang')
        text = request.POST.get('text')

        translated = GoogleTranslator(source=sourceLang,target=targetLang).translate(text)

        document = Document()

        section = document.sections[0]

        style = document.styles['Normal']
        font = style.font
        font.name = 'Arial'

        section.top_margin = Cm(1.27)
        section.bottom_margin = Cm(1.27)
        section.left_margin = Cm(1.27)
        section.right_margin = Cm(1.27)

        p = document.add_paragraph(translated)

        buffer = BytesIO()
        document.save(buffer)
        buffer.seek(0)

        
        return FileResponse(
            buffer,
            as_attachment=True,
            filename="report.docx",
            content_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )


    return render(request, 'pages/translation.html')