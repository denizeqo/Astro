from .motherChart import MotherChart
import json





class DailyChart(MotherChart):

    

    @property
    def planets(self):

        super().setOrbiteMinDistance(25, 14)
        planets = super().planets

        with open(MotherChart.ephePath + "\\planetNum.json","r") as file:
            planetsNum = json.load(file)

        for planet in planets:
            planetName = planet['name']

            if planetsNum.get(planetName, -1) == -1:
                planet['num']['value'] = MotherChart.degMin(planet['position'])
                planet['num']['sup'] = ''
                planet['num']['color'] = '#ffffff'
                continue

            if planet['num']['sup'] == '':

                if planet['num']['value'] not in planetsNum[planetName]["B"]:
                    planet['num']['value'] = MotherChart.degMin(planet['position'])
                    planet['num']['color'] = '#ffffff'
            
            else:
                if planet['num']['value'] not in planetsNum[planetName]["A"]:
                    planet['num']['value'] = MotherChart.degMin(planet['position'])
                    planet['num']['sup'] = ''
                    planet['num']['color'] = '#ffffff'
        
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

        for angle in fourAngles:
            if angle['name'] == 'IC' or angle['name'] == 'Desc':
                angle['num']['value'] = ''
                angle['num']['sup'] = ''

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

            for star in stars:
                starIndex = int(star.get('position') // 2.5)
                starName = star.get('name')
                starColor = star.get('color')

                if planetIndex == starIndex:

                    if planetName in addedPlanets:
                        starsForPlanet[starsForPlanetIndex]['stars'].append({'starName':starName, 'starColor':starColor})
                        
                    else:
                        starsForPlanet.append({'planetName':planetName, 'planetColor':planetColor, 'stars':[{'starName':starName, 'starColor':starColor}]})
                        addedPlanets.add(planetName)
                        starsForPlanetIndex += 1
        
        return starsForPlanet

