from .motherChart import MotherChart
from ..models import DailyCalendar, MonthlyCalendar
import json

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo



class DailyChart(MotherChart):

    def __init__(self, lat, lng, dateOfBirth, timeOfBirth, firstName, lastName, city, country):
        super().__init__(lat, lng, dateOfBirth, timeOfBirth, firstName, lastName, city, country)

    @property
    def planets(self):

        super().setOrbiteMinDistance(15, 10)
        planets = super().planets

        with open(MotherChart.ephePath + "\\planetNum.json","r") as file:
            planetsNum = json.load(file)

        for planet in planets:
            planetName = planet['name']

            if planetName == "New Moon" or planetName == "Full Moon":
                if planet['num']['sup'] != '':
                    planet['num']['value'] = DailyChart.numAbove(planet['num']['value'])

                continue


            if planetsNum.get(planetName, -1) == -1:
                planet['num']['value'] = str(int(planet['position'])) + '° '
                planet['num']['sup'] = ''
                planet['num']['color'] = '#ffffff'
                continue

            if planet['num']['sup'] == '':

                if planet['num']['value'] not in planetsNum[planetName]["B"]:
                    planet['num']['value'] = str(int(planet['position'])) + '° '
                    planet['num']['color'] = '#ffffff'
            
            else:
                if planet['num']['value'] not in planetsNum[planetName]["A"]:
                    planet['num']['value'] = str(int(planet['position'])) + '° '
                    planet['num']['sup'] = ''
                    planet['num']['color'] = '#ffffff'

                else:    
                    planet['num']['value'] = DailyChart.numAbove(planet['num']['value'])
            
        
        return planets
    
    
    
    @property
    def stars(self):
        stars = super().stars
        for star in stars:
            star['num']['value'] = ''
            star['num']['sup'] = ''
            star['num']['color'] = '#ffffff'
        
        return stars
    

    @property
    def fourAngles(self):

        fourAngles = super().fourAngles

        with open(MotherChart.ephePath + "\\planetNum.json","r") as file:
            planetsNum = json.load(file)
            

        for angle in fourAngles:

            angleName = angle['name']

            if angleName== 'IC' or angleName == 'Desc':
                angle['num']['value'] = ''
                angle['num']['sup'] = ''
                continue

            if planetsNum.get(angleName, -1) == -1:
                angle['num']['value'] = str(int(angle['position'])) + '° '
                angle['num']['sup'] = ''
                angle['num']['color'] = '#ffffff'
                continue
            
            if angle['num']['sup'] == '':

                if angle['num']['value'] not in planetsNum[angleName]["B"]:
                    angle['num']['value'] = str(int(angle['position'])) + '° '
                    angle['num']['color'] = '#ffffff'
            
            else:
                if angle['num']['value'] not in planetsNum[angleName]["A"]:
                    angle['num']['value'] = str(int(angle['position'])) + '° '
                    angle['num']['sup'] = ''
                    angle['num']['color'] = '#ffffff'

                else:    
                    angle['num']['value'] = DailyChart.numAbove(angle['num']['value'])
            
        return fourAngles



    def getStarsForPlanet(self):
        stars = super().stars
        planets = super().planets

        starsForPlanet = []
        addedPlanets = set()
        starsForPlanetIndex = -1

        for planet in planets:
            planetIndex = int(planet.get('position') // 2.5)
            planetName = planet.get('name')
            planetColor = planet.get('color')
            planetHouseNum = int(planet.get('house').get('num'))
            planetHouseSymbol = planet.get('house').get('symbol')
            planetPosition = MotherChart.degMin(planet.get('position'))
            planetMovement = planet.get('movement')

            if 'Moon' in planetName:
                planetDailyCalendar = DailyCalendar.objects.get(name='Moon')
            else:
                planetDailyCalendar = DailyCalendar.objects.get(name=planetName)

            
            if planetDailyCalendar.numIndex == planetIndex:
                planetDailyDescription = planetDailyCalendar.description
            else:
                planetDailyDescription = ''
                planetDailyCalendar.description = ''
                planetDailyCalendar.numIndex = planetIndex
                planetDailyCalendar.save()
    
    
            planetData = {'planetName':planetName, 
                          'planetColor':planetColor, 
                          'planetPosition':planetPosition, 
                          'planetHouseNum':planetHouseNum, 
                          'planetHouseSymbol':planetHouseSymbol, 
                          'planetDailyDescription':planetDailyDescription,
                          'planetMovement' : planetMovement,
                          'stars':[]}
            
            starsForPlanet.append(planetData)
            starsForPlanetIndex += 1

            for star in stars:
                starIndex = int(star.get('position') // 2.5)
                starName = star.get('name')
                starColor = star.get('color')

                if planetIndex == starIndex:
                    starsForPlanet[starsForPlanetIndex]['stars'].append({'starName':starName, 'starColor':starColor})    
        
        return starsForPlanet
    
    def getMonthlyCalendar(self):

        startDate = datetime.now(ZoneInfo("Europe/Rome"))
        endDate = startDate + timedelta(hours=700)

        objects = MonthlyCalendar.objects.filter(timestamp__range=(startDate, endDate))
        colorMap = self.objectsColorMap

        results = []

        for object in objects:
            results.append({
                'id':object.id,
                'date': object.timestamp.strftime("%Y-%m-%d"),
                'time': object.timestamp.strftime("%H:%M"),
                'name': object.name,
                'house': object.houseNum,
                'houseSymbol': object.houseSymbol,
                'position': object.position,
                'description': object.description,
                'color': colorMap[object.name]
            })

        return results


    
    @staticmethod
    def numAbove(num:int):

        if num in [20, 30, 40, 50, 60, 70, 80, 90]:
            return num
        
        num = int(str(num)[::-1])

        return num


