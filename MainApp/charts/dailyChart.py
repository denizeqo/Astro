from .motherChart import MotherChart
from ..models import DailyCalendar, MonthlyCalendar
import json
from django.utils import timezone

from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo



class DailyChart():

    def __init__(self, lat, lng, dateOfBirth, timeOfBirth, firstName, lastName, city, country):
        self.birthChart = MotherChart(lat, lng, dateOfBirth, timeOfBirth, firstName, lastName, city, country)

        self.currentDate = timezone.now().strftime("%Y-%m-%d")
        self.currentTime = timezone.now().strftime("%H:%M")

        self.todayChart = MotherChart(lat, lng, self.currentDate, self.currentTime, firstName, lastName, city, country)

        self.lastOrbiteObjects = self.todayChart.lastOrbiteObjects
        self.firstOrbiteObjects = self.todayChart.firstOrbiteObjects + ["New Moon", "First Quarter Moon", "Full Moon", "Last Quarter Moon", "Falling Moon", "Rising Moon"]
        self.objectList = self.todayChart.objects

        self.birthChartStars = self.birthChart.stars
        self.birthChartFourAngles = self.birthChart.fourAngles
        self.birthChartUserData = self.birthChart.userData
        self.birthChartTalisman = self.birthChart.talisman


        self.todayChartPlanets = self.todayChart.planets
        self.todayChartStars = self.todayChart.stars
        self.todayChartFourAngles = self.todayChart.fourAngles
        self.todayChartUserData = self.todayChart.userData
        self.todayChartTalisman = self.todayChart.talisman

    @property
    def birthChartPlanets(self):

        planetsToRemove = ['Pluto', 'Chiron']
        planets = []

        for planet in self.birthChart.planets:
            #if planet['name'] in planetsToRemove:
             #   continue
            
            planet['color'] = planet['color'] + '70'
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

        return self.birthChartStars + self.todayChartStars



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