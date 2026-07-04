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



class Num:

    NumSymbols = ['D', 'T', 'B', 'G', 'L', 'V', 'P', 'A', 'H', 'K', 'U', 'P']
    NumSymbolsColor = ['#E3242B', '#7BB369', '#EEDEC5', '#0077BE', '#FFEA99', '#9F8C76', '#008000', '#880808', '#FFAF3D', '#808080', '#4E9FE5', '#8968CD']

    def __init__(self, planetPosition:float):
        self.planetPosition = planetPosition
        self.houseIndex = int(planetPosition/30)
        self.symbolIndex = int(planetPosition/2.5)
        self.numSup = '' if self.symbolIndex + 1 <= 99 else Num.NumSymbols[(self.houseIndex + self.symbolIndex) % 12]
        self.numSupColor = '' if self.symbolIndex + 1 <= 99 else Num.NumSymbolsColor[(self.houseIndex + self.symbolIndex) % 12]
        

    @property
    def numValue(self):
        num = int((self.planetPosition / 2.5) + 1)
        if num >= 100:
            num = (num - 100) + 28

        return num     

    @property
    def numColor(self):
        colorMap = {
                0: '#ffffff',
                1: '#E3242b',
                2: '#4e9fe5'
            }
    
        yellowNum = [4, 13, 16, 22, 31, 40, 49, 58, 67, 76, 85, 94]
        if self.numValue in yellowNum:
            return '#ffea99'
        
        return colorMap[self.numValue % 3]
    

    def to_dict(self):
        return {'value':self.numValue, 'color':self.numColor, 'sup':self.numSup, 'supColor':self.numSupColor}

    
     

class MotherChart:

    tf = TimezoneFinder()
    ephePath = "C:\\Users\\User\\OneDrive\\Desktop\\Dei\\Project\\Eureka\\Astro\\Astro\\sweph\\ephe"
    

    def __init__(self, lat:float, lng:float, dateOfBirth:str, timeOfBirth:str, firstName:str, lastName:str, city:str, country:str):

        self.firstName = firstName
        self.lastName = lastName
        self.city = city
        self.country = country
        self.dateOfBirth = dateOfBirth
        self.timeOfBirth = timeOfBirth

        self.lat, self.lng = MotherChart.getLonLat(lat, lng)
        self.utcDateOfBirth, self.utcTimeOfBirth = MotherChart.getUTCDateTime(dateOfBirth, timeOfBirth, lat, lng, MotherChart.tf)
        self.date = Datetime(self.utcDateOfBirth, self.utcTimeOfBirth, '+00:00')
        self.pos = GeoPos(self.lat, self.lng)

        self.objects = [
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

        self.fourAnglesNames = [const.ASC, const.MC, const.IC, const.DESC]
        self.aspectsList = [0, 60, 90, 120, 150, 180] 
        self.aspectsTypeMap = {
            0: 'Alignment',
            60: 'Sextile',
            90: 'Square',
            120: 'Trine',
            150: 'Quincunx',
            180: 'Synchronization',
        }

        self.objectsColorMap = {
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
            const.SOUTH_NODE: '#AAD5DB',
            "New Moon": '#AAD5DB',
            "First Quarter Moon": '#AAD5DB',
            "Full Moon": '#AAD5DB',
            "Last Quarter Moon":'#AAD5DB'
        } 

        self.talismanObjects = [
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

        self.houseSymbols = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 'Libra', 'Scorpion', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        self.lastOrbiteObjects = [const.SATURN, const.URANUS, const.NEPTUNE, const.PLUTO, const.CHIRON]
        self.lastOrbiteMinDistance = 6
        self.firstOrbiteObjects = [const.MOON, const.NORTH_NODE, const.SOUTH_NODE]
        self.firstOrbiteMinDistance = 15

        swe.set_ephe_path(MotherChart.ephePath)
        self.chart = Chart(self.date, self.pos, IDs=self.objects)


    def setOrbiteMinDistance(self, firstOrbite, lastOrbite):
        self.lastOrbiteMinDistance = lastOrbite
        self.firstOrbiteMinDistance = firstOrbite


    @property
    def moonPhase(self):

        phase_angle = (self.chart.get(const.MOON).lon - self.chart.get(const.SUN).lon) % 360

        if phase_angle < 45 or phase_angle >= 315:
            phase = "New Moon"
        elif phase_angle < 135:
            phase = "First Quarter Moon"
        elif phase_angle < 225:
            phase = "Full Moon"
        else:
            phase = "Last Quarter Moon"

        return phase


    @property
    def planets(self):

        lastOrbitePlanetsPositions = self._getPlanetSymbolPosition(self.lastOrbiteObjects, False)
        firstOrbitePlanetsPositions =  self._getPlanetSymbolPosition(self.firstOrbiteObjects, True)

        planets = []

        for planet in self.objects:

            if planet in self.lastOrbiteObjects:
                symbolPosition = lastOrbitePlanetsPositions[planet]
                
            elif planet in self.firstOrbiteObjects:
                symbolPosition = firstOrbitePlanetsPositions[planet]

            else:
                symbolPosition = self.chart.get(planet).lon

            planetName = planet
            if planet == const.MOON:
                planetName = self.moonPhase
            
            planets.append({
                'name':planetName,
                'movement':self.chart.get(planet).movement()[0],
                'position':self.chart.get(planet).lon,
                'symbolPosition': symbolPosition,
                'color': self.objectsColorMap[planetName],
                'num': Num(self.chart.get(planet).lon).to_dict(),
                'house':self.getObjectHouse(self.chart.get(planet).lon)
            })

        return planets

    @property
    def fourAngles(self):

        fourAngles = []

        for i in self.fourAnglesNames:
            fourAngles.append({
                'name':i,
                'position': self.chart.get(i).lon,
                'color': self.objectsColorMap[i],
                'num': Num(self.chart.get(i).lon).to_dict(),
                'house': self.getObjectHouse(self.chart.get(i).lon)
            })
        
        return fourAngles
    

    @property
    def stars(self):

        ascIndex = [int(i['position']/2.5) for i in self.fourAngles]
        planetsIndex = [int(i['position']/2.5) for i in self.planets]

        starOrbite = 0
        stars = []

        with open(MotherChart.ephePath + "\\stars2.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        for index in range(len(data)):
            starPosition = data[index]["topicalDeg"]

            if int(starPosition/2.5) in planetsIndex or int(starPosition/2.5) in ascIndex:

                if len(stars) != 0:
                    lastStarPosition = stars[len(stars)-1]["position"]

                    if starPosition - lastStarPosition >= 1:
                        starOrbite = 0

                stars.append({'name': data[index]['name'],
                              'position': starPosition,
                              'color':data[index]['color'], 
                              'num':Num(starPosition).to_dict(), 
                              'orbite':starOrbite,
                              'house':self.getObjectHouse(starPosition)})

                if starOrbite >= 4:
                    starOrbite = 0
                else:
                    starOrbite += 1
        
        return stars
    

    @property
    def aspects(self):
        allObjects = self.objects + self.fourAnglesNames

        aspects = []
        for i in range(len(allObjects)):
            for j in range(i + 1, len(allObjects)):
                asp = getAspect(self.chart.get(allObjects[i]), self.chart.get(allObjects[j]), self.aspectsList)
                if asp and asp.type != -1 and asp.orb <= 2.5:
                    aspects.append({'active': asp.active.id,
                                    'activeColor': self.objectsColorMap[asp.active.id],
                                    'passive': asp.passive.id,
                                    'passiveColor': self.objectsColorMap[asp.passive.id],
                                    'orb':asp.orb,
                                    'type':self.aspectsTypeMap[asp.type] + ' ' + str(asp.type) + '°',
                                    'movement':asp.active.movement})
        return aspects


    @property
    def talisman(self):

        talisman = []

        for object in self.talismanObjects:
            talisman.append(Num(self.chart.get(object).lon).to_dict())

        return talisman
    

    @property
    def userData(self):
        return {'First Name': self.firstName, 
                'Last Name': self.lastName, 
                'City': self.city,
                'Country': self.country,
                'Latitude': self.lat,
                'Longitude': self.lng,
                'LocalTime': self.dateOfBirth + ' ' + self.timeOfBirth,
                'UTCTime': self.utcDateOfBirth.replace('/', '-') + ' ' + self.utcTimeOfBirth[:5],
                'Talisman': self.talisman}
        



    def getObjectHouse(self, position:float):

        houseNum = (position // 30) + 1
        houseSymbol = self.houseSymbols[int(position // 30)]

        return {'num':houseNum, 'symbol':houseSymbol}
    

    def _getPlanetSymbolPosition(self, objects:list, isFirstOrbite:bool):

        objects = dict(sorted([(object, self.chart.get(object).lon) for object in objects], key=lambda item: item[1]))
        minDistance = self.firstOrbiteMinDistance if isFirstOrbite else self.lastOrbiteMinDistance

        lastPosition = -1
        for objectName in objects:

            if lastPosition == -1:
                lastPosition = objects[objectName]
                continue
            
            diffDistance = objects[objectName] - lastPosition

            if diffDistance <= minDistance:
                objects[objectName] += minDistance - diffDistance
            
            lastPosition = objects[objectName]
        
        return objects


    @staticmethod
    def getLonLat(lat:float, lon:float):

        latDeg = int(lat)
        latMin =int((lat - latDeg) * 60)
        direction = 'n' if latDeg >= 0 else 's'
        latStr = str(abs(latDeg)) + direction + str(latMin)

        lonDeg = int(lon)
        lonMin = int((lon - lonDeg) * 60)
        direction = 'e' if lonDeg >= 0 else 'w'
        lonStr = str(abs(lonDeg)) + direction + str(lonMin)

        return latStr, lonStr


    @staticmethod
    def getUTCDateTime(date:str, time:str, lat:float, lng:float, tf:TimezoneFinder):
    
        tz_name = tf.timezone_at(lat=lat, lng=lng)

        fmt = "%Y-%m-%d %H:%M"
        dateTime = date + ' ' + time
        dt = datetime.strptime(dateTime, fmt)

        tz = pytz.timezone(tz_name)
        local_dt = tz.localize(dt, is_dst=None)

        utcDateTime = str(local_dt.astimezone(pytz.UTC)).split('+')[0]

        utcDate = '/'.join(utcDateTime.split(' ')[0].split('-'))
        utcTime = utcDateTime.split(' ')[1]

        return utcDate, utcTime
    
    @staticmethod
    def degMin(deg):

        intDeg = int(deg)
        min = int((deg - intDeg) * 60)

        return str(intDeg) + '° ' + str(min) + "'"

    
    







