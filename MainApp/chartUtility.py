from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import json

from django.conf import settings
from pathlib import Path
from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
from flatlib.aspects import getAspect
import flatlib.aspects as aspects
import swisseph as swe

from docx.shared import RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Cm
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT, WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_ROW_HEIGHT_RULE, WD_ALIGN_VERTICAL


tf = TimezoneFinder()

def getLonLat(lat, lon):

    latDeg = int(lat)
    latMin =int((lat - latDeg) * 60)
    direction = 'n' if latDeg >= 0 else 's'
    latStr = str(abs(latDeg)) + direction + str(latMin)

    lonDeg = int(lon)
    lonMin = int((lon - lonDeg) * 60)
    direction = 'e' if lonDeg >= 0 else 'w'
    lonStr = str(abs(lonDeg)) + direction + str(lonMin)

    return latStr, lonStr


def getUTCDateTime(date, time, lat, lon):
    
    tz_name = tf.timezone_at(lat=lat, lng=lon)

    fmt = "%Y-%m-%d %H:%M"
    dateTime = date + ' ' + time
    dt = datetime.strptime(dateTime, fmt)

    tz = pytz.timezone(tz_name)
    local_dt = tz.localize(dt, is_dst=None)

    utcDateTime = str(local_dt.astimezone(pytz.UTC)).split('+')[0]

    utcDate = '/'.join(utcDateTime.split(' ')[0].split('-'))
    utcTime = utcDateTime.split(' ')[1]

    return utcDate, utcTime


def getStars(planets, fourAngles):

    ascIndex = [int(i['position']/2.5) for i in fourAngles]
    planetsIndex = [int(i['position']/2.5) for i in planets]

    starOrbite = 0
    stars = []

    with open(Path(settings.BASE_DIR) / "sweph" / "ephe" / "stars2.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for index in range(len(data)):
        starPosition = data[index]["topicalDeg"]

        if int(starPosition/2.5) in planetsIndex or int(starPosition/2.5) in ascIndex:

            if len(stars) != 0:
                lastStarPosition = stars[len(stars)-1]["position"]

                if starPosition - lastStarPosition >= 1:
                    starOrbite = 0

            stars.append({'name': data[index]['name'], "position": starPosition,'color':data[index]['color'], 'num':getChartNum(starPosition), 'orbite':starOrbite, 'house': getHouse(starPosition)})

            if starOrbite >= 4:
                starOrbite = 0
            else:
                starOrbite += 1
    
    return stars 

DEFAULT_OBJECTS = [
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

DEFAULT_ANGLES = [const.ASC, const.MC, const.IC, const.DESC]

def createChart(latitude, longitude, dateOfBirth, timeOfBirth, objects=None):

    if objects is None:
        objects = DEFAULT_OBJECTS

    lat, lon = getLonLat(latitude, longitude)
    dateOfBirth, timeOfBirth = getUTCDateTime(dateOfBirth, timeOfBirth, latitude, longitude)

    swe.set_ephe_path(str(Path(settings.BASE_DIR) / "sweph" / "ephe"))

    date = Datetime(dateOfBirth, timeOfBirth, '+00:00')
    pos = GeoPos(lat, lon)
    chart = Chart(date, pos, IDs=objects)

    return chart


def getFourAngles(chart, names=None):

    if names is None:
        names = DEFAULT_ANGLES

    angle_color_map = {
        const.ASC: '#E3242B',
        const.MC: '#808080',
        const.IC: '#4E9FE5',
        const.DESC: '#a8e4a0',
    }

    fourAngles = []
    for name in names:
        obj = chart.get(name)
        fourAngles.append({
            'name': name,
            'position': obj.lon,
            'color': angle_color_map.get(name, '#ffffff'),
            'num': getChartNum(obj.lon),
            'house': getHouse(obj.lon),
        })

    return fourAngles


def getPlanets(chart, objects=None):

    if objects is None:
        objects = DEFAULT_OBJECTS

    planetsColorMap = {
        const.SUN: '#FFEA99',
        const.MOON: '#AAD5DB',
        const.MERCURY: '#cdb891',
        const.VENUS: '#a8e4a0',
        const.MARS: '#E3242B',
        const.JUPITER: '#FFAF3D',
        const.SATURN: '#808080',
        const.URANUS: '#4E9FE5',
        const.NEPTUNE: '#8968CD',
        const.PLUTO: '#ffffff',
        const.CHIRON: '#ffffff',
        const.NORTH_NODE: '#AAD5DB',
        const.SOUTH_NODE: '#AAD5DB'
    }

    lastOrbitePlanets = [const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO, const.CHIRON]
    firstOrbitePlanets = [const.MOON, const.NORTH_NODE, const.SOUTH_NODE]

    # Only compute symbol positions for orbite groups that are actually charted
    lastOrbiteRequested = [p for p in lastOrbitePlanets if p in objects]
    firstOrbiteRequested = [p for p in firstOrbitePlanets if p in objects]

    lastOrbitePlanetsPositions = _getPlanetSymbolPosition(chart, lastOrbiteRequested, False) if lastOrbiteRequested else {}
    firstOrbitePlanetsPositions = _getPlanetSymbolPosition(chart, firstOrbiteRequested, True) if firstOrbiteRequested else {}

    planets = []
    for planet in objects:

        if planet in lastOrbitePlanetsPositions:
            symbolPosition = lastOrbitePlanetsPositions[planet]
        elif planet in firstOrbitePlanetsPositions:
            symbolPosition = firstOrbitePlanetsPositions[planet]
        else:
            symbolPosition = chart.get(planet).lon

        planetName = planet 
        if planet == const.MOON:

            phase_angle = (chart.get(const.MOON).lon - chart.get(const.SUN).lon) % 360

            if phase_angle < 45 or phase_angle >= 315:
                planetName = "New Moon"
            elif phase_angle < 135:
                planetName = "First Quarter Moon"
            elif phase_angle < 225:
                planetName = "Full Moon"
            else:
                planetName = "Last Quarter Moon"
            

        planets.append({'name':planetName, 'movement':chart.get(planet).movement()[0], 'position':chart.get(planet).lon, 'symbolPosition':symbolPosition, 'color':planetsColorMap[planet], 'num':getChartNum(chart.get(planet).lon), 'house':getHouse(chart.get(planet).lon)})
        
    return planets

        
def getChartSymbols(asc):

    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpion', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

    results = []
    houseNum = int(asc/30) - 1
    for i in range(144):

        if i % 12 == 0:
            houseNum += 1

        signsIndex = (i + houseNum) % 12
        results.append(signs[signsIndex])

    return results


def getUserData(chart, latitude, longitude, dateOfBirth, timeOfBirth, firstName, lastName, city, country, objects=None):

    lat, lng = getLonLat(latitude, longitude)
    utcDateOfBirth, utcTimeOfBirth = getUTCDateTime(dateOfBirth, timeOfBirth, latitude, longitude)
    talismanNum = _getTalismanNum(chart, objects)
    userData = {'First Name':firstName, 'Last Name':lastName, 'City':city, 'Country':country, 'Latitude':lat, 'Longitude':lng, 'Local Time':dateOfBirth + ' ' + timeOfBirth, 'UTC Time':utcDateOfBirth.replace('/', '-') + ' ' + utcTimeOfBirth[:5], 'talisman':talismanNum}

    return userData


def getChartNum(position):

    num = _getChartNumValue(position)
    sup, supColor = _getChartNumSymbol(position)
    color = _getChartNumColor(num)

    return {'value': num, 'sup': sup, 'color':color, 'supColor':supColor}

def _getTalismanNum(chart, objects=None):

    if objects is None:
        objects = [
            const.ASC,
            const.MC,
            const.SUN,
            const.MOON,
            const.MERCURY,
            const.VENUS,
            const.MARS,
            const.JUPITER,
            const.SATURN,
            const.URANUS,
            const.NEPTUNE,
            const.NORTH_NODE,
            const.SOUTH_NODE,
        ]

    results = []

    for object in objects:
        results.append(getChartNum(chart.get(object).lon))

    return results

def _getChartNumSymbol(position):

    signs = ['D', 'T', 'B', 'G', 'L', 'V', 'P', 'A', 'H', 'K', 'U', 'P']
    signsColor = ['#E3242B', '#7BB369', '#EEDEC5', '#0077BE', '#FFEA99', '#9F8C76', '#008000', '#880808', '#FFAF3D', '#808080', '#4E9FE5', '#8968CD']

    houseNum = int(position/30)
    symbolNum = int(position/2.5)

    if symbolNum + 1 <= 99:
        return '', ''
    
    singsIndex = (houseNum + symbolNum) % 12

    return signs[singsIndex], signsColor[singsIndex]



def _getChartNumValue(position):

    num = int((position/2.5) + 1)
    if num >= 100:
        num = (num - 100) + 28

    return num

def _getChartNumColor(num):
    
    colorMap = {
                0: '#ffffff',
                1: '#E3242b',
                2: '#4e9fe5'
            }
    
    yellowNum = [4, 13, 16, 22, 31, 40, 49, 58, 67, 76, 85, 94]
    if num in yellowNum:
        return '#ffea99'
    
    return colorMap[num % 3]


def _getPlanetSymbolPosition(chart, planets, isFirstOrbite):

    planets = dict(sorted([(i, chart.get(i).lon) for i in planets], key=lambda item: item[1]))

    lastPosition = -1

    if isFirstOrbite:
        minDistance = 15
    else:
        minDistance = 6
    
    for i in planets:

        if lastPosition == -1:
            lastPosition = planets[i]
            continue
        
        diffDistance = planets[i] - lastPosition
        if diffDistance <= minDistance:
            planets[i] += minDistance - diffDistance
        
        lastPosition = planets[i]
    
    return planets


def getHouse(position):

    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpion', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    houseNum = (position // 30) + 1
    houseSymbol = signs[int(position // 30)]

    return {'num': houseNum, 'symbol':houseSymbol}


def get_all_aspects(chart, objects=None):
    
    result = []

    planetsColorMap = {
        const.ASC: '#E3242B',
        const.MC: '#808080',
        const.IC: '#4E9FE5',
        const.DESC: '#a8e4a0',
        const.SUN: '#FFEA99',
        const.MOON: '#AAD5DB',
        const.MERCURY: '#cdb891',
        const.VENUS: '#a8e4a0',
        const.MARS: '#E3242B',
        const.JUPITER: '#FFAF3D',
        const.SATURN: '#808080',
        const.URANUS: '#4E9FE5',
        const.NEPTUNE: '#8968CD',
        const.PLUTO: '#ffffff',
        const.CHIRON: '#ffffff',
        const.NORTH_NODE: '#AAD5DB',
        const.SOUTH_NODE: '#AAD5DB'
    }   

    if objects is None:
        objects = list(planetsColorMap.keys())

    objs = [chart.get(i) for i in objects]

    aspList = [0, 60, 90, 120, 150, 180]


    aspects.MAX_EXACT_ORB = 0

    aspectType = {
        0: 'Alignment',
        60: 'Sextile',
        90: 'Square',
        120: 'Trine',
        150: 'Quincunx',
        180: 'Synchronization',
    }

    for i in range(len(objs)):
        for j in range(i + 1, len(objs)):
            asp = getAspect(objs[i], objs[j], aspList)
            if asp and asp.type != -1 and asp.orb <= 2.5:
                result.append({'active':asp.active.id, 'activeColor':planetsColorMap[asp.active.id], 'passive':asp.passive.id, 'passiveColor':planetsColorMap[asp.passive.id], 'orb':asp.orb, 'type':aspectType[asp.type] + ' ' + str(asp.type) + '°', 'movement':asp.active.movement})


    return result


def degMin(deg):

    intDeg = int(deg)
    min = int((deg - intDeg) * 60)

    return str(intDeg) + '° ' + str(min) + "'"

def set_cell_border(cell):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    tcBorders = OxmlElement('w:tcBorders')

    for border_name in ['top', 'left', 'bottom', 'right']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '8')       # border thickness
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), 'ffffff')
        tcBorders.append(border)

    tcPr.append(tcBorders)

def create_planet_table(doc, asc_list):
    # Force new page    
    doc.add_page_break() 

    # Optional title on second page    
    title = doc.add_paragraph() 
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER   
    run = title.add_run("The Planet Positions of Your Birth")
    run.font.name =   'Bahnschrift Light Condensed'
    run.font.color.rgb = RGBColor.from_string('EDE1FF')   
    run.font.size = Pt(36)   

    # Define table headers    
    headers = ["Name", "Sign", "House", "Degree", "Num", "Move" ]  

    # Create table    
    table = doc.add_table(rows=1, cols=len(headers))    

    #table.style = 'Table Grid'  # adds borders automatically  

    # Fill header row    
    header_cells = table.rows[0].cells 
    table.rows.height = Cm(2)
   # table.rows.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY

    for i, h in enumerate(headers):        
        paragraph = header_cells[i].paragraphs[0]        
        run = paragraph.add_run(h) 
        run.font.name = 'Poppins'       
        run.bold = True        
        run.font.size = Pt(11)

        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        header_cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER        
       # set_cell_border(header_cells[i]) 

    # Fill table rows    
    for i, item in enumerate(asc_list):        
        row = table.add_row()

        if i == 1:
            row.height = Cm(2)
        else:
            row.height = Cm(1)

        row.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY

        row_cells = row.cells

        row_cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER 
        p1 = row_cells[0].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_before = 0
        p1.paragraph_format.space_after = 0

        run1 = p1.add_run(str(item.get("name", "")))
        run1.font.name = 'Poppins'
        run1.font.color.rgb = RGBColor.from_string(item.get('color')[1:])

        row_cells[1].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p2 = row_cells[1].paragraphs[0]
        p2.paragraph_format.space_before = 0
        p2.paragraph_format.space_after = 0

        run2 = p2.add_run(str(item.get("house", {})['symbol']))    
        run2.font.name = 'Poppins'

        row_cells[2].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p3 = row_cells[2].paragraphs[0]
        p3.paragraph_format.space_before = 0
        p3.paragraph_format.space_after = 0

        run3 = p3.add_run(str(item.get("house", {})['num'])) 
        run3.font.name = 'Poppins'

        row_cells[3].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p4 = row_cells[3].paragraphs[0]
        p4.paragraph_format.space_before = 0
        p4.paragraph_format.space_after = 0

        run4 = p4.add_run(degMin(round(item.get("position", 0), 2)))
        run4.font.name = 'Poppins'


        row_cells[4].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p5 = row_cells[4].paragraphs[0]
        p5.paragraph_format.space_before = 0
        p5.paragraph_format.space_after = 0

        run5 = p5.add_run(str(item.get("num", {})['value']))
        run5.font.name = 'Poppins'
        run5.font.color.rgb = RGBColor.from_string(item.get("num", {})['color'][1:])

        if item.get("num", {})['sup'] != '':
            run6 = p5.add_run(item.get("num", {})['sup'])
            run6.font.name = 'Poppins'
            run6.font.color.rgb = RGBColor.from_string(item.get("num", {})['supColor'][1:])

        
        row_cells[5].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p6 = row_cells[5].paragraphs[0]
        p6.paragraph_format.space_before = 0
        p6.paragraph_format.space_after = 0

        run7 = p6.add_run(str(item.get("movement", ""))) 
        run7.font.name = 'Poppins'

        # Add borders to every cell        
        for cell in row_cells:
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER        
            set_cell_border(cell)



def creat_stars_table(doc, star_list):
    # Force new page    
    doc.add_page_break() 

    # Optional title on second page    
    title = doc.add_paragraph() 
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER   
    run = title.add_run("The Star Positions of Your Birth")
    run.font.name =   'Bahnschrift Light Condensed'
    run.font.color.rgb = RGBColor.from_string('EDE1FF')   
    run.font.size = Pt(36)   

    # Define table headers    
    headers = ["Star", "Sign", "House", "Degree", "Num"]  

    # Create table    
    table = doc.add_table(rows=1, cols=len(headers))    

    #table.style = 'Table Grid'  # adds borders automatically  

    # Fill header row    
    header_cells = table.rows[0].cells 
    table.rows.height = Cm(2)
   # table.rows.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY

    for i, h in enumerate(headers):        
        paragraph = header_cells[i].paragraphs[0]        
        run = paragraph.add_run(h) 
        run.font.name = 'Poppins'       
        run.bold = True        
        run.font.size = Pt(11)

        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        header_cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER        
       # set_cell_border(header_cells[i]) 

    # Fill table rows    
    for item in star_list:        
        row = table.add_row()
        row.height = Cm(1)
        row.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY

        row_cells = row.cells

        row_cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER 
        p1 = row_cells[0].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_before = 0
        p1.paragraph_format.space_after = 0

        run1 = p1.add_run(str(item.get("name", "")))
        run1.font.name = 'Poppins'
        run1.font.color.rgb = RGBColor.from_string(item.get('color')[1:])

        row_cells[1].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p2 = row_cells[1].paragraphs[0]
        p2.paragraph_format.space_before = 0
        p2.paragraph_format.space_after = 0

        run2 = p2.add_run(str(item.get("house", {})['symbol']))    
        run2.font.name = 'Poppins'

        row_cells[2].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p3 = row_cells[2].paragraphs[0]
        p3.paragraph_format.space_before = 0
        p3.paragraph_format.space_after = 0

        run3 = p3.add_run(str(item.get("house", {})['num'])) 
        run3.font.name = 'Poppins'

        row_cells[3].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p4 = row_cells[3].paragraphs[0]
        p4.paragraph_format.space_before = 0
        p4.paragraph_format.space_after = 0

        run4 = p4.add_run(degMin(round(item.get("position", 0), 2))) 
        run4.font.name = 'Poppins'


        row_cells[4].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p5 = row_cells[4].paragraphs[0]
        p5.paragraph_format.space_before = 0
        p5.paragraph_format.space_after = 0

        run5 = p5.add_run(str(item.get("num", {})['value']))
        run5.font.name = 'Poppins'
        run5.font.color.rgb = RGBColor.from_string(item.get("num", {})['color'][1:])

        if item.get("num", {})['sup'] != '':
            run6 = p5.add_run(item.get("num", {})['sup'])
            run6.font.name = 'Poppins'
            run6.font.color.rgb = RGBColor.from_string(item.get("num", {})['supColor'][1:])

        # Add borders to every cell        
        for cell in row_cells:
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER        
            set_cell_border(cell)


def creat_asc_table(doc, asc_list):
    # Force new page    
    doc.add_page_break() 

    # Optional title on second page    
    title = doc.add_paragraph() 
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER   
    run = title.add_run("The Four Angles of Your Birth")
    run.font.name =   'Bahnschrift Light Condensed'
    run.font.color.rgb = RGBColor.from_string('EDE1FF')   
    run.font.size = Pt(36)   

    # Define table headers    
    headers = ["Four Angles", "Sign", "House", "Degree", "Num"]  

    # Create table    
    table = doc.add_table(rows=1, cols=len(headers))    

    #table.style = 'Table Grid'  # adds borders automatically  

    # Fill header row    
    header_cells = table.rows[0].cells 
    table.rows.height = Cm(2)
   # table.rows.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY

    for i, h in enumerate(headers):        
        paragraph = header_cells[i].paragraphs[0]        
        run = paragraph.add_run(h) 
        run.font.name = 'Poppins'       
        run.bold = True        
        run.font.size = Pt(11)

        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        header_cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER        
       # set_cell_border(header_cells[i]) 

    # Fill table rows    
    for item in asc_list:        
        row = table.add_row()
        row.height = Cm(1)
        row.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY

        row_cells = row.cells

        row_cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER 
        p1 = row_cells[0].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_before = 0
        p1.paragraph_format.space_after = 0

        run1 = p1.add_run(str(item.get("name", "")))
        run1.font.name = 'Poppins'
        run1.font.color.rgb = RGBColor.from_string(item.get('color')[1:])

        row_cells[1].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p2 = row_cells[1].paragraphs[0]
        p2.paragraph_format.space_before = 0
        p2.paragraph_format.space_after = 0

        run2 = p2.add_run(str(item.get("house", {})['symbol']))    
        run2.font.name = 'Poppins'

        row_cells[2].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p3 = row_cells[2].paragraphs[0]
        p3.paragraph_format.space_before = 0
        p3.paragraph_format.space_after = 0

        run3 = p3.add_run(str(item.get("house", {})['num'])) 
        run3.font.name = 'Poppins'

        row_cells[3].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p4 = row_cells[3].paragraphs[0]
        p4.paragraph_format.space_before = 0
        p4.paragraph_format.space_after = 0

        run4 = p4.add_run(degMin(round(item.get("position", 0), 2))) 
        run4.font.name = 'Poppins'


        row_cells[4].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p5 = row_cells[4].paragraphs[0]
        p5.paragraph_format.space_before = 0
        p5.paragraph_format.space_after = 0

        run5 = p5.add_run(str(item.get("num", {})['value']))
        run5.font.name = 'Poppins'
        run5.font.color.rgb = RGBColor.from_string(item.get("num", {})['color'][1:])

        if item.get("num", {})['sup'] != '':
            run6 = p5.add_run(item.get("num", {})['sup'])
            run6.font.name = 'Poppins'
            run6.font.color.rgb = RGBColor.from_string(item.get("num", {})['supColor'][1:])

        # Add borders to every cell        
        for cell in row_cells:
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER        
            set_cell_border(cell)


def creat_aspects_table(doc, aspects_list):
    # Force new page    
    doc.add_page_break() 

    # Optional title on second page    
    title = doc.add_paragraph() 
    title.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER   
    run = title.add_run("The Aspects of Your Birth")
    run.font.name =   'Bahnschrift Light Condensed'
    run.font.color.rgb = RGBColor.from_string('EDE1FF')   
    run.font.size = Pt(36)   

    # Define table headers    
    headers = ["Planet", "Aspect", "Planet", "Orb", "Move"]  

    # Create table    
    table = doc.add_table(rows=1, cols=len(headers))    
 

    # Fill header row    
    header_cells = table.rows[0].cells 
    table.rows.height = Cm(2)

    for i, h in enumerate(headers):        
        paragraph = header_cells[i].paragraphs[0]        
        run = paragraph.add_run(h) 
        run.font.name = 'Poppins'       
        run.bold = True        
        run.font.size = Pt(11)

        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        header_cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER        
       # set_cell_border(header_cells[i]) 

    # Fill table rows    
    for item in aspects_list:        
        row = table.add_row()
        row.height = Cm(1)
        row.height_rule = WD_ROW_HEIGHT_RULE.EXACTLY

        row_cells = row.cells

        row_cells[0].vertical_alignment = WD_ALIGN_VERTICAL.CENTER 
        p1 = row_cells[0].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_before = 0
        p1.paragraph_format.space_after = 0

        run1 = p1.add_run(str(item.get("active", "")))
        run1.font.name = 'Poppins'
        run1.font.color.rgb = RGBColor.from_string(item.get('activeColor')[1:])

        row_cells[1].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p2 = row_cells[1].paragraphs[0]
        p2.paragraph_format.space_before = 0
        p2.paragraph_format.space_after = 0

        run2 = p2.add_run(str(item.get("type", "")))    
        run2.font.name = 'Poppins'

        row_cells[2].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p3 = row_cells[2].paragraphs[0]
        p3.paragraph_format.space_before = 0
        p3.paragraph_format.space_after = 0

        run3 = p3.add_run(str(item.get("passive", ""))) 
        run3.font.name = 'Poppins'
        run3.font.color.rgb = RGBColor.from_string(item.get('passiveColor')[1:])

        row_cells[3].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p4 = row_cells[3].paragraphs[0]
        p4.paragraph_format.space_before = 0
        p4.paragraph_format.space_after = 0

        run4 = p4.add_run(degMin(round(item.get("orb", 0),2))) 
        run4.font.name = 'Poppins'


        row_cells[4].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p5 = row_cells[4].paragraphs[0]
        p5.paragraph_format.space_before = 0
        p5.paragraph_format.space_after = 0

        run5 = p5.add_run(item.get("movement", ""))
        run5.font.name = 'Poppins'

        # Add borders to every cell        
        for cell in row_cells:
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER        
            set_cell_border(cell)
