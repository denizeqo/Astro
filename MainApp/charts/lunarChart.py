import json
import math
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo

from flatlib import const
from flatlib.aspects import getAspect

from .motherChart import MotherChart, Num


class LunarChart:
    """28 Lunar Mansions chart ("Horoskopi Ditor Lunar").

    Reference points: Moon, Ascendant, Sun, Saturn and the Lunar Nodes.
    Produces two plain-dict payloads from the same base chart:
    - ``birth``  -> Lunar Birth Horoscope (natal date/time)
    - ``moment`` -> Daily Lunar Horoscope (defaults to 'now' at the given place)
    All returned data is JSON-serializable.
    """

    MANSION_SIZE = 360 / 28  # 12°51'26"
    ECLIPSE_ORB = 12

    referenceObjects = [const.MOON, const.ASC, const.SUN, const.SATURN, const.NORTH_NODE, const.SOUTH_NODE]

    glyphs = {
        const.MOON: '☽',
        const.ASC: 'ASC',
        const.SUN: '☉',
        const.SATURN: '♄',
        const.NORTH_NODE: '☊',
        const.SOUTH_NODE: '☋',
    }

    aspectsList = [0, 30, 60, 90, 120, 150, 180]

    def __init__(self, lat: float, lng: float, dateOfBirth: str, timeOfBirth: str,
                 firstName: str, lastName: str, city: str, country: str,
                 date: str = None, time: str = None, lang: str = 'en'):

        self.lang = lang if lang in ('en', 'de', 'fr', 'it') else 'en'

        with open(Path(MotherChart.ephePath) / 'lunarMansions.json', 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.birthChart = MotherChart(lat, lng, dateOfBirth, timeOfBirth,
                                      firstName, lastName, city, country)

        if date is None or time is None:
            tzName = MotherChart.tf.timezone_at(lat=lat, lng=lng) or 'UTC'
            now = datetime.now(ZoneInfo(tzName))
            date = now.strftime('%Y-%m-%d')
            time = now.strftime('%H:%M')

        self.momentChart = MotherChart(lat, lng, date, time,
                                       firstName, lastName, city, country)

    # ---------------------------------------------------------------
    # Static data
    # ---------------------------------------------------------------

    def _t(self, translations: dict) -> dict:
        return translations.get(self.lang) or translations.get('en', {})

    @property
    def mansions(self):
        mansions = []
        for mansion in self.data['mansions']:
            ruler = self.data['rulers'][mansion['ruler']]
            start = (mansion['number'] - 1) * self.MANSION_SIZE
            mansions.append({
                'number': mansion['number'],
                'name': mansion['name'],
                'title': self._t(mansion['translations']).get('title', ''),
                'description': self._t(mansion['translations']).get('description', ''),
                'ruler': mansion['ruler'],
                'rulerGlyph': ruler['glyph'],
                'rulerColor': ruler['color'],
                'startDeg': round(start, 4),
                'endDeg': round(start + self.MANSION_SIZE, 4),
                'image': mansion['image'],
            })
        return mansions

    def mansionOf(self, lon: float) -> int:
        return min(int(lon % 360 / self.MANSION_SIZE) + 1, 28)

    # ---------------------------------------------------------------
    # Lunar phase & eclipse
    # ---------------------------------------------------------------

    def moonPhase(self, chart: MotherChart):
        elongation = (chart.chart.get(const.MOON).lon - chart.chart.get(const.SUN).lon) % 360
        index = int(((elongation + 22.5) % 360) / 45)
        phase = self.data['phases'][index]
        illumination = (1 - math.cos(math.radians(elongation))) / 2
        return {
            'key': phase['key'],
            'index': index,
            'name': self._t(phase['translations']),
            'glyph': phase['glyph'],
            'elongation': round(elongation, 2),
            'illumination': round(illumination * 100, 1),
        }

    def eclipse(self, chart: MotherChart, phase: dict):
        moonLon = chart.chart.get(const.MOON).lon
        nodeDistance = min(
            abs((moonLon - chart.chart.get(const.NORTH_NODE).lon + 180) % 360 - 180),
            abs((moonLon - chart.chart.get(const.SOUTH_NODE).lon + 180) % 360 - 180),
        )

        eclipseKey = None
        if phase['key'] == 'new':
            eclipseKey = 'solar'
        elif phase['key'] == 'full':
            eclipseKey = 'lunar'

        if eclipseKey is None or nodeDistance > self.ECLIPSE_ORB:
            return None

        eclipse = self.data['eclipses'][eclipseKey]
        return {
            'type': eclipseKey,
            'name': self._t(eclipse['translations']),
            'glyph': eclipse['glyph'],
            'nodeDistance': round(nodeDistance, 2),
        }

    # ---------------------------------------------------------------
    # Reference points & aspects
    # ---------------------------------------------------------------

    def referencePoints(self, chart: MotherChart):
        colorMap = chart.objectsColorMap
        points = []
        for objectId in self.referenceObjects:
            lon = chart.chart.get(objectId).lon
            mansionNumber = self.mansionOf(lon)
            mansion = self.mansions[mansionNumber - 1]
            points.append({
                'name': objectId,
                'glyph': self.glyphs[objectId],
                'position': lon,
                'color': colorMap[objectId],
                'num': Num(lon).to_dict(),
                'house': chart.getObjectHouse(lon),
                'mansion': {'number': mansionNumber, 'name': mansion['name'], 'title': mansion['title']},
            })
        return points

    def aspects(self, chart: MotherChart):
        colorMap = chart.objectsColorMap
        typeMap = chart.aspectsTypeMap
        categoryOf = {
            const.MOON: 'lunar',
            const.SUN: 'solar',
            const.ASC: 'ascendant',
            const.SATURN: 'saturn',
            const.NORTH_NODE: 'nodal',
            const.SOUTH_NODE: 'nodal',
        }
        priority = ['lunar', 'solar', 'ascendant', 'saturn', 'nodal']

        aspects = []
        for i in range(len(self.referenceObjects)):
            for j in range(i + 1, len(self.referenceObjects)):
                asp = getAspect(chart.chart.get(self.referenceObjects[i]),
                                chart.chart.get(self.referenceObjects[j]),
                                self.aspectsList)
                if asp and asp.type != -1 and asp.orb <= 2.5:
                    categories = sorted([categoryOf[asp.active.id], categoryOf[asp.passive.id]],
                                        key=priority.index)
                    aspects.append({
                        'active': asp.active.id,
                        'activeColor': colorMap[asp.active.id],
                        'passive': asp.passive.id,
                        'passiveColor': colorMap[asp.passive.id],
                        'orb': chart.degMin(asp.orb),
                        'type': typeMap[asp.type] + ' ' + str(asp.type) + '°',
                        'deg': str(asp.type),
                        'movement': asp.active.movement,
                        'category': categories[0],
                        'activePosition': chart.chart.get(asp.active.id).lon,
                        'passivePosition': chart.chart.get(asp.passive.id).lon,
                    })
        return aspects

    # ---------------------------------------------------------------
    # Payloads
    # ---------------------------------------------------------------

    def _payload(self, chart: MotherChart):
        phase = self.moonPhase(chart)
        moonMansionNumber = self.mansionOf(chart.chart.get(const.MOON).lon)
        moonMansion = dict(self.mansions[moonMansionNumber - 1])
        moonMansion['progress'] = round(
            (chart.chart.get(const.MOON).lon % self.MANSION_SIZE) / self.MANSION_SIZE * 100, 1)

        return {
            'asc': chart.chart.get(const.ASC).lon,
            'moonPhase': phase,
            'eclipse': self.eclipse(chart, phase),
            'moonMansion': moonMansion,
            'referencePoints': self.referencePoints(chart),
            'aspects': self.aspects(chart),
            'userData': chart.userData,
        }

    @property
    def birth(self):
        return self._payload(self.birthChart)

    @property
    def moment(self):
        return self._payload(self.momentChart)

    def to_dict(self):
        return {
            'mansionSizeLabel': self.data['mansionSizeLabel'],
            'mansions': self.mansions,
            'birth': self.birth,
            'moment': self.moment,
        }

