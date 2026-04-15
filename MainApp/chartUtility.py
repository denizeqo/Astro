from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import json

from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
from flatlib.aspects import getAspect
import swisseph as swe


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

                if starPosition - lastStarPosition >= 1.2:
                    starOrbite = 0

            stars.append({'name': data[index]['name'], "position": starPosition, 'num':getChartNum(starPosition), 'orbite':starOrbite, 'house': getHouse(starPosition)})

            if starOrbite >= 6:
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

        planets.append({'name':planet, 'movement':chart.get(planet).movement()[0], 'position':chart.get(planet).lon, 'symbolPosition':symbolPosition, 'color':planetsColorMap[planet], 'num':getChartNum(chart.get(planet).lon), 'house':getHouse(chart.get(planet).lon)})
        
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


def getChartNum(position):

    num = _getChartNumValue(position)
    sup = _getChartNumSymbol(position)
    color = _getChartNumColor(num)

    return {'value': num, 'sup': sup, 'color':color}



def _getChartNumSymbol(position):

    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpion', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']

    houseNum = int(position/30)
    symbolNum = int(position/2.5)

    if symbolNum + 1 <= 99:
        return ''
    
    singsIndex = (houseNum + symbolNum) % 12

    return signs[singsIndex][:2].upper()



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
    objs = list(chart.objects)
    result = []

    major = [
        const.CONJUNCTION,
        const.SEXTILE,
        const.SQUARE,
        const.TRINE,
        const.OPPOSITION
    ]

    for i in range(len(objs)):
        for j in range(i + 1, len(objs)):
            asp = getAspect(objs[i], objs[j], major)
            if asp:
                result.append(asp)

    return result
    





