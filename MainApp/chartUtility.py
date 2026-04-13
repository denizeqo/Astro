from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import json

from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const
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
    
    planets = [
        {'name':'Sun', 'position':chart.get(const.SUN).lon, 'color':'#FFEA99', 'num':getChartNum(chart.get(const.SUN).lon), 'house':getHouse(chart.get(const.SUN).lon)},
        {'name':'Moon', 'position':chart.get(const.MOON).lon, 'color':'#AAD5DB', 'num':getChartNum(chart.get(const.MOON).lon), 'house':getHouse(chart.get(const.MOON).lon)},
        {'name':'North Moon', 'position':chart.get(const.NORTH_NODE).lon, 'color':'#AAD5DB', 'num':getChartNum(chart.get(const.NORTH_NODE).lon), 'house':getHouse(chart.get(const.NORTH_NODE).lon)},
        {'name':'South Moon', 'position':chart.get(const.SOUTH_NODE).lon, 'color':'#AAD5DB', 'num':getChartNum(chart.get(const.SOUTH_NODE).lon), 'house':getHouse(chart.get(const.SOUTH_NODE).lon)},
        {'name':'Mercury', 'position':chart.get(const.MERCURY).lon, 'color':'#cdb891', 'num':getChartNum(chart.get(const.MERCURY).lon), 'house':getHouse(chart.get(const.MERCURY).lon)},
        {'name':'Venus', 'position':chart.get(const.VENUS).lon, 'color':'#a8e4a0', 'num':getChartNum(chart.get(const.VENUS).lon), 'house':getHouse(chart.get(const.VENUS).lon)},
        {'name':'Mars', 'position':chart.get(const.MARS).lon, 'color':'#E3242B', 'num':getChartNum(chart.get(const.MARS).lon), 'house':getHouse(chart.get(const.MARS).lon)},
        {'name':'Jupiter', 'position':chart.get(const.JUPITER).lon, 'color':'#FFAF3D', 'num':getChartNum(chart.get(const.JUPITER).lon), 'house':getHouse(chart.get(const.JUPITER).lon)},
        {'name':'Saturn', 'position':chart.get(const.SATURN).lon, 'color':'#808080', 'num':getChartNum(chart.get(const.SATURN).lon), 'house':getHouse(chart.get(const.SATURN).lon)},
        {'name':'Uranus', 'position':chart.get(const.URANUS).lon, 'color':'#4E9FE5', 'num':getChartNum(chart.get(const.URANUS).lon), 'house':getHouse(chart.get(const.URANUS).lon)},
        {'name':'Neptune', 'position':chart.get(const.NEPTUNE).lon, 'color':'#8968CD', 'num':getChartNum(chart.get(const.NEPTUNE).lon), 'house':getHouse(chart.get(const.NEPTUNE).lon)},
        {'name':'Pluto', 'position':chart.get(const.PLUTO).lon, 'color':'#ffffff', 'num':getChartNum(chart.get(const.PLUTO).lon), 'house':getHouse(chart.get(const.PLUTO).lon)},
        {'name':'Chiron', 'position':chart.get(const.CHIRON).lon, 'color':'#ffffff', 'num':getChartNum(chart.get(const.CHIRON).lon), 'house':getHouse(chart.get(const.CHIRON).lon)},
    ]

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


def getHouse(position):

    signs = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpion', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
    houseNum = (position // 30) + 1
    houseSymbol = signs[int(position // 30)]

    return {'num': houseNum, 'symbol':houseSymbol}
    





