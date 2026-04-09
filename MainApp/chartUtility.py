from timezonefinder import TimezoneFinder
from datetime import datetime
import pytz
import json


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


def getStarsData(planets, asc):

    ascIndex = [int(i/2.5) for i in asc.values()]
    planetsIndex = [int(i/2.5) for i in planets.values()]

    stars = []
    with open("C:\\Users\\User\\OneDrive\\Desktop\\Dei\\Project\\Eureka\\Astro\\Astro\\sweph\\ephe\\stars2.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    for star in data:
        starPosition = star["topicalDeg"]

        if int(starPosition/2.5) in planetsIndex or int(starPosition/2.5) in ascIndex:
            stars.append({'name': star['name'], "topicalDeg": starPosition, 'starNum':int(starPosition/2.5)})
    
    return stars 