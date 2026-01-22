from flatlib.chart import Chart
from flatlib.datetime import Datetime
from flatlib.geopos import GeoPos
from flatlib import const

date = Datetime('2005/06/20', '12:10', '+02:00')
pos = GeoPos('41n7', '20e48')
chart = Chart(date, pos)

asc = chart.get(const.ASC)
sun = chart.get(const.SUN)
print(sun.lon)
print(asc.lon)
