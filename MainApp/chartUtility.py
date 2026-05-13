from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import json

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
from docx.shared import Pt
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT


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

    with open("C:\\Users\\User\\OneDrive\\Desktop\\Dei\\Project\\Eureka\\Astro\\Astro\\sweph\\ephe\\stars2.json", "r", encoding="utf-8") as f:
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

def createChart(latitude, longitude, dateOfBirth, timeOfBirth):

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

    lat, lon = getLonLat(latitude, longitude)
    dateOfBirth, timeOfBirth = getUTCDateTime(dateOfBirth, timeOfBirth, latitude, longitude)

    swe.set_ephe_path(r"C:\\Users\\User\\OneDrive\\Desktop\\Dei\\Project\\Eureka\\Astro\\Astro\\sweph\\ephe")

    date = Datetime(dateOfBirth, timeOfBirth, '+00:00')
    pos = GeoPos(lat, lon)
    chart = Chart(date, pos, IDs=objects)

    return chart


def getFourAngles(chart):

    fourAngles = [
        {'name':'ASC', 'position':chart.get(const.ASC).lon, 'color':'#E3242B', 'num':getChartNum(chart.get(const.ASC).lon), 'house':getHouse(chart.get(const.ASC).lon)},
        {'name':'MC', 'position':chart.get(const.MC).lon, 'color':'#808080', 'num':getChartNum(chart.get(const.MC).lon), 'house':getHouse(chart.get(const.MC).lon)},
        {'name':'IC', 'position':chart.get(const.IC).lon, 'color':'#4E9FE5', 'num':getChartNum(chart.get(const.IC).lon), 'house':getHouse(chart.get(const.IC).lon)},
        {'name':'DSC', 'position':chart.get(const.DESC).lon, 'color':'#a8e4a0', 'num':getChartNum(chart.get(const.DESC).lon), 'house':getHouse(chart.get(const.DESC).lon)}
    ]

    return fourAngles


def getPlanets(chart):

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

    lastOrbitePlanetsPositions = _getPlanetSymbolPosition(chart, lastOrbitePlanets, False)
    firstOrbitePlanetsPositions =  _getPlanetSymbolPosition(chart, firstOrbitePlanets, True)

    planets = []
    for planet in planetsColorMap:

        if planet in lastOrbitePlanets:
            symbolPosition = lastOrbitePlanetsPositions[planet]
        elif planet in firstOrbitePlanets:
            symbolPosition = firstOrbitePlanetsPositions[planet]
        else:
            symbolPosition = chart.get(planet).lon

        planetName = planet 
        if planet == const.MOON:
            asp = getAspect(chart.get(const.MOON), chart.get(const.SUN), const.MAJOR_ASPECTS)

            if asp and asp.type != -1 and asp.orb <= 2.5:
                if asp.type == 0:
                    planetName  = 'New Moon'
                elif asp.type == 180:
                    planetName = 'Full Moon'
                else:
                    planetName = 'Moon'
                

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


def getUserData(chart, latitude, longitude, dateOfBirth, timeOfBirth, firstName, lastName, city, country):

    lat, lng = getLonLat(latitude, longitude)
    utcDateOfBirth, utcTimeOfBirth = getUTCDateTime(dateOfBirth, timeOfBirth, latitude, longitude)
    talismanNum = _getTalismanNum(chart)
    userData = {'First Name':firstName, 'Last Name':lastName, 'City':city, 'Country':country, 'Latitude':lat, 'Longitude':lng, 'Local Time':dateOfBirth + ' ' + timeOfBirth, 'UTC Time':utcDateOfBirth.replace('/', '-') + ' ' + utcTimeOfBirth[:5], 'talisman':talismanNum}

    return userData


def getChartNum(position):

    num = _getChartNumValue(position)
    sup, supColor = _getChartNumSymbol(position)
    color = _getChartNumColor(num)

    return {'value': num, 'sup': sup, 'color':color, 'supColor':supColor}

def _getTalismanNum(chart):

    objectList = [
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
        const.SOUTH_NODE
    ]

    results = []

    for object in objectList:
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


def get_all_aspects(chart):
    
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

    objs = [chart.get(i) for i in planetsColorMap.keys()]

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
    

def addTableRows(table, userData):

    def _getKeyValue():
        for key, value in userData.items():
            yield key, value

    gen = _getKeyValue()
    talismanIndex = 0

    for i in range(4):
        key1, value1 = next(gen)

        if key1 == 'talisman':
            break

        key2, value2 = next(gen)

        row = table.add_row()
        cell = row.cells[0]
        p = cell.paragraphs[0]
        p.add_run(f'{key1}: {value1}').bold = True

        cell = row.cells[1]
        p = cell.paragraphs[0]
        p.add_run(f'{key2}: {value2}').bold = True

        cell = row.cells[2]
        p = cell.paragraphs[0]
        spaces = 15


        for j in range(3):
            p.add_run('    ')
            pValue = str(userData['talisman'][talismanIndex + j]['value']) + userData['talisman'][talismanIndex + j]['sup']
            color = userData['talisman'][talismanIndex + j]['color'][1:]

            run = p.add_run(pValue)
            run.font.color.rgb = RGBColor.from_string(color if color != 'ffffff' else '808080')
            run.bold = True

            p.add_run(' ' * (spaces - len(pValue) * 2))

        talismanIndex += 3


def set_cell_border(cell):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()

    tcBorders = OxmlElement('w:tcBorders')

    for border_name in ['top', 'left', 'bottom', 'right']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '8')       # border thickness
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), '000000')
        tcBorders.append(border)

    tcPr.append(tcBorders)


def create_planet_table(doc, planet_list):    
    # Force new page    
    doc.add_page_break() 

    # Optional title on second page    
    title = doc.add_paragraph()    
    run = title.add_run("Planet Table")    
    run.bold = True    
    run.font.size = Pt(16)   

    # Define table headers    
    headers = ["Name", "Movement", "Position", "Num", "Sign", "House" ]  

    # Create table    
    table = doc.add_table(rows=1, cols=len(headers))    
    table.style = 'Table Grid'  # adds borders automatically  

    # Fill header row    
    header_cells = table.rows[0].cells    
    for i, h in enumerate(headers):        
        paragraph = header_cells[i].paragraphs[0]        
        run = paragraph.add_run(h)        
        run.bold = True        
        run.font.size = Pt(11)

        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        header_cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER        
        set_cell_border(header_cells[i]) 

    # Fill table rows    
    for item in planet_list:        
        row_cells = table.add_row().cells        
        row_cells[0].text = str(item.get("name", ""))        
        row_cells[1].text = str(item.get("movement", ""))        
        row_cells[2].text = str(round(item.get("position", 0), 2))               
        row_cells[3].text = str(            
            str(item.get("num", {})['value']) +            
            item.get("num", {})['sup']        )        
        row_cells[4].text = str(item.get("house", {})['symbol'])
        row_cells[5].text = str(item.get("house", {})['num'])

        # Add borders to every cell        
        for cell in row_cells:
            cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER            
            set_cell_border(cell)

def creat_stars_table(doc, stars_list):
    # Force new page    
    doc.add_page_break() 

    # Optional title on second page    
    title = doc.add_paragraph()    
    run = title.add_run("Star Table")    
    run.bold = True    
    run.font.size = Pt(16)   

    # Define table headers    
    headers = ["Star", "Sign", "House", "Degree", "Num"]  

    # Create table    
    table = doc.add_table(rows=1, cols=len(headers))    
    table.style = 'Table Grid'  # adds borders automatically  

    # Fill header row    
    header_cells = table.rows[0].cells    
    for i, h in enumerate(headers):        
        paragraph = header_cells[i].paragraphs[0]        
        run = paragraph.add_run(h)        
        run.bold = True        
        run.font.size = Pt(11)

        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        header_cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER        
        set_cell_border(header_cells[i]) 

    # Fill table rows    
    for item in stars_list:        
        row_cells = table.add_row().cells        
        row_cells[0].text = str(item.get("name", ""))    
        row_cells[1].text = str(item.get("house", {})['symbol'])   
        row_cells[2].text = str(item.get("house", {})['num'])         
        row_cells[3].text = str(round(item.get("position", 0), 2))               
        row_cells[4].text = str(            
            str(item.get("num", {})['value']) +            
            item.get("num", {})['sup']        )        

        # Add borders to every cell        
        for cell in row_cells:
            cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER            
            set_cell_border(cell)

def creat_asc_table(doc, asc_list):
    # Force new page    
    doc.add_page_break() 

    # Optional title on second page    
    title = doc.add_paragraph()    
    run = title.add_run("Four Angles Table")    
    run.bold = True    
    run.font.size = Pt(16)   

    # Define table headers    
    headers = ["Four Angles", "Sign", "House", "Degree", "Num"]  

    # Create table    
    table = doc.add_table(rows=1, cols=len(headers))    
    table.style = 'Table Grid'  # adds borders automatically  

    # Fill header row    
    header_cells = table.rows[0].cells    
    for i, h in enumerate(headers):        
        paragraph = header_cells[i].paragraphs[0]        
        run = paragraph.add_run(h)        
        run.bold = True        
        run.font.size = Pt(11)

        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        header_cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER        
        set_cell_border(header_cells[i]) 

    # Fill table rows    
    for item in asc_list:        
        row_cells = table.add_row().cells        
        row_cells[0].text = str(item.get("name", ""))    
        row_cells[1].text = str(item.get("house", {})['symbol'])     
        row_cells[2].text = str(item.get("house", {})['num'])       
        row_cells[3].text = str(round(item.get("position", 0), 2))               
        row_cells[4].text = str(            
            str(item.get("num", {})['value']) +            
            item.get("num", {})['sup']        )        

        # Add borders to every cell        
        for cell in row_cells:
            cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER            
            set_cell_border(cell)


def creat_aspects_table(doc, aspects_list):
    # Force new page    
    doc.add_page_break() 

    # Optional title on second page    
    title = doc.add_paragraph()    
    run = title.add_run("Aspects Table")    
    run.bold = True    
    run.font.size = Pt(16)   

    # Define table headers    
    headers = ["Planet", "Aspect", "Planet", "Orb", "Move"]  

    # Create table    
    table = doc.add_table(rows=1, cols=len(headers))    
    table.style = 'Table Grid'  # adds borders automatically  

    # Fill header row    
    header_cells = table.rows[0].cells    
    for i, h in enumerate(headers):        
        paragraph = header_cells[i].paragraphs[0]        
        run = paragraph.add_run(h)        
        run.bold = True        
        run.font.size = Pt(11)

        paragraph.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
        header_cells[i].vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER        
        set_cell_border(header_cells[i]) 

    # Fill table rows    
    for item in aspects_list:        
        row_cells = table.add_row().cells        
        row_cells[0].text = str(item.get("active", ""))                
        row_cells[1].text = str(item.get("type", ""))                      
        row_cells[2].text = str(item.get("passive", ""))
        row_cells[3].text = str(round(item.get("orb", 0),2))
        row_cells[4].text = str(item.get("movement", ""))

        # Add borders to every cell        
        for cell in row_cells:
            cell.paragraphs[0].alignment = WD_PARAGRAPH_ALIGNMENT.CENTER
            cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER            
            set_cell_border(cell)
