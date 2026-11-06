from .motherChart import MotherChart
from ..models import DailyCalendar, MonthlyCalendar
import json
from pathlib import Path
from django.utils import timezone

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from django.utils.translation import gettext as _
from django.utils.html import format_html, format_html_join

class DailyChart():

    def __init__(self, lat, lng, dateOfBirth, timeOfBirth, firstName, lastName, city, country, date, time):
        self.birthChart = MotherChart(lat, lng, dateOfBirth, timeOfBirth, firstName, lastName, city, country)

        self.currentDate = timezone.now().strftime("%Y-%m-%d")
        self.currentTime = timezone.now().strftime("%H:%M")

        self.todayChart = MotherChart(lat, lng, date, time, firstName, lastName, city, country)

        self.lastOrbiteObjects = self.todayChart.lastOrbiteObjects
        self.firstOrbiteObjects = self.todayChart.firstOrbiteObjects + ["New Moon", "First Quarter Moon", "Full Moon", "Last Quarter Moon", "Falling Moon", "Rising Moon"]
        self.objectList = self.todayChart.objects

        self.birthChartStars = self.birthChart.stars
        self.birthChartFourAngles = self.birthChart.fourAngles
        self.birthChartUserData = self.birthChart.userData
        self.birthChartTalisman = self.birthChart.talisman

        self.todayChartStars = self.todayChart.stars
        self.todayChartFourAngles = self.todayChart.fourAngles
        self.todayChartUserData = self.todayChart.userData
        self.todayChartTalisman = self.todayChart.talisman



    @property
    def todayChartPlanets(self):
        
        planets = self.todayChart.planets

        with open(Path(MotherChart.ephePath) / "planetNum.json","r") as file:
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
    def birthChartPlanets(self):

        planetsToRemove = ['Pluto', 'Chiron']
        planets = []

        for planet in self.birthChart.planets:
            #if planet['name'] in planetsToRemove:
             #   continue
            planet['num']['value'] = ''
            planet['num']['sup'] = ''
            planet['color'] = "#dddcdcff"
            planets.append(planet)
        
        return planets
    

    @property
    def combinePlanets(self):

        planets = []

        todayLastOrbiteObjects = [i for i in self.todayChartPlanets if i['name'] in self.lastOrbiteObjects]
        birthLastOrbiteObjects = [i for i in self.birthChartPlanets if i['name'] in self.lastOrbiteObjects]

        allLastOrbiteObjects = todayLastOrbiteObjects + birthLastOrbiteObjects

        todayFirstOrbiteObjects = [i for i in self.todayChartPlanets if i['name'] in self.firstOrbiteObjects]
        birthFirstOrbiteObjects = [i for i in self.birthChartPlanets if i['name'] in self.firstOrbiteObjects]
        
        allFirstOrbiteObjects = todayFirstOrbiteObjects + birthFirstOrbiteObjects

        planets += self._getPlanetSymbolPosition(allFirstOrbiteObjects, 15)
        planets += self._getPlanetSymbolPosition(allLastOrbiteObjects, 6)

        allObjects = self.todayChartPlanets + self.birthChartPlanets

        dis = 13
        for object in self.objectList:

            if object in self.lastOrbiteObjects or object in self.firstOrbiteObjects:
                continue

            obj = []

            for i in self.birthChartPlanets:
                if i['name'] == object:
                    obj.append(i)

            for j in self.todayChartPlanets:
                if j['name'] == object:
                    obj.append(j)
            
            planets += self._getPlanetSymbolPosition(obj, dis)

            dis-=1

        return planets
    


    @property
    def combineStars(self):

        stars = self.birthChartStars + self.todayChartStars
        
        for star in stars:

            star['num']['value'] = ''
            star['num']['sup'] = ''

        return stars


    def _getPlanetSymbolPosition(self, objects:list, minDistance:int):

            objects = sorted(objects, key=lambda item: item['symbolPosition'])

            lastPosition = -1
            for object in objects:

                if lastPosition == -1:
                    lastPosition = object['symbolPosition']
                    continue
                
                diffDistance = object['symbolPosition'] - lastPosition

                if diffDistance <= minDistance:
                    object['symbolPosition'] += minDistance - diffDistance
                
                lastPosition = object['symbolPosition']
            
            return objects
    

    @staticmethod
    def numAbove(num:int):

        if num in [20, 30, 40, 50, 60, 70, 80, 90]:
            return num
        
        num = int(str(num)[::-1])

        return num
    
    def getStarsForPlanet(self):
        stars =  self.todayChart.stars
        planets =  self.todayChart.planets

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


            planetData = {'planetName':planetName, 
                            'planetColor':planetColor, 
                            'planetPosition':planetPosition, 
                            'planetHouseNum':planetHouseNum, 
                            'planetHouseSymbol':planetHouseSymbol,
                            'planetMovement' : planetMovement,
                            'num':planet['num'],
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



    @staticmethod
    def getPlanetTitle(planet: dict) -> dict:
        planetName = _(planet["planetName"])
        planetColor = planet["planetColor"]
        houseNum = planet["planetHouseNum"]
        houseSymbol = _(planet["planetHouseSymbol"])
        movement = _(planet["planetMovement"])
        position = planet["planetPosition"]

        stars = planet.get("stars", [])

        # ----------------------------
        # Plain star names
        # ----------------------------

        starNames = [
            star["starName"]
            for star in stars
        ]

        starsText = ", ".join(starNames)

        # ----------------------------
        # Colored star names for HTML
        # ----------------------------

        starsHtml = format_html_join(
            ", ",
            '<span style="color:{}; font-family: \'Poppins\', sans-serif; text-align: center;">{}</span>',
            (
                (
                    star["starColor"],
                    star["starName"]
                )
                for star in stars
            )
        )

        # ----------------------------
        # First row
        # ----------------------------

        firstLine = _(
            "%(planet)s is at House %(house)s (%(sign)s) %(movement)s"
        ) % {
            "planet": planetName,
            "house": houseNum,
            "sign": houseSymbol,
            "movement": movement,
        }

        firstLineHtml = format_html(
            _(
                "{planet} is at House {house} ({sign}) {movement}"
            ),
            planet=format_html(
                '<span style="color:{}; font-family: \'Poppins\', sans-serif; text-align: center;">{}</span>',
                planetColor,
                planetName
            ),
            house=houseNum,
            sign=houseSymbol,
            movement=movement,
        )

        # ----------------------------
        # Second row
        # ----------------------------

        if stars:

            secondLine = _(
                "It is at %(position)s aligned with stars %(stars)s"
            ) % {
                "position": position,
                "stars": starsText,
            }

            secondLineHtml = format_html(
                _(
                    "It is at {position} aligned with stars {stars}"
                ),
                position=position,
                stars=starsHtml,
            )

        else:

            secondLine = _(
                "It is at %(position)s"
            ) % {
                "position": position,
            }

            secondLineHtml = format_html(
                _("It is at {position}"),
                position=position,
            )

        # ----------------------------
        # Final result
        # ----------------------------

        return {
            "title": firstLine + "\n" + secondLine,
            "titleHtml": str(
                format_html(
                    "{}<br>{}",
                    firstLineHtml,
                    secondLineHtml
                )
            )
        }
    
    @staticmethod
    def getTransitTitle(planet: dict) -> dict:

        planetName = _(planet["name"])
        planetColor = planet["color"]

        houseNum = planet["house"]["num"]
        houseSymbol = _(planet["house"]["symbol"])

        titleTemplate = _(
            "Transit {planet} in House {house} ({sign})"
        )

        # Plain text
        title = titleTemplate.format(
            planet=planetName,
            house=houseNum,
            sign=houseSymbol
        )

        # HTML version with colored planet name
        titleHtml = format_html(
            titleTemplate,
            planet=format_html(
                '<span style="color:{}; font-family: \'Poppins\', sans-serif; text-align: left;">{}</span>',
                planetColor,
                planetName
            ),
            house=houseNum,
            sign=houseSymbol
        )

        return {
            "title": title,
            "titleHtml": str(titleHtml)
        }