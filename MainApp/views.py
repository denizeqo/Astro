from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
from django.http import JsonResponse

# Create your views here.
def Home(request):

    if request.method == 'POST':

        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        dateOfBirth = request.POST.get('dateOfBirth')
        timeOfBirth = request.POST.get('timeOfBirth')
        country = request.POST.get('country')
        city = request.POST.get('city')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')

        dateOfBirth = dateOfBirth.split('-')

        yearOfBirth = dateOfBirth[0]
        monthOfBirth = dateOfBirth[1]
        dayOfBirth = dateOfBirth[2]

        timeOfBirth = timeOfBirth.split(':')

        hourOfBirth = timeOfBirth[0]
        minuteOfBirth = timeOfBirth[1]

        url = "https://horoscopes.astro-seek.com/calculate-birth-chart-horoscope-online/"
        params = {
                "input_natal": 1,
                "send_calculation": 1,
                "narozeni_den": int(dayOfBirth), #day
                "narozeni_mesic": int(monthOfBirth), #month
                "narozeni_rok": int(yearOfBirth), #year

                "narozeni_hodina": int(hourOfBirth), #hours
                "narozeni_minuta": int(minuteOfBirth), #minutes
                "narozeni_sekunda": 00, #sekonda

                "narozeni_city":'',
                "narozeni_mesto_hidden": "Manually place: °'N, °'E", #

                "narozeni_stat_hidden":'',
                "narozeni_podstat_kratky_hidden":'',

                "narozeni_sirka_stupne": float(latitude), #latitude deg
                "narozeni_sirka_minuty": 0, #latitude min
                "narozeni_sirka_smer": 0, #north

                "narozeni_delka_stupne": float(longitude), #longitude deg
                "narozeni_delka_minuty": 0, #longitude min
                "narozeni_delka_smer": 0, #east

                "narozeni_timezone_form": 'auto',
                "narozeni_timezone_dst_form": 'auto',

                "hid_fortune":1,
                "hid_fortune_check":'on',
                "hid_vertex":1,
                "hid_vertex_check":'on',
                "hid_chiron":1,
                "hid_chiron_check":'on',
                "hid_lilith":1,
                "hid_lilith_check":'on',
                "hid_uzel":1,
                "hid_uzel_check":'on',

                "house_system":"Placidus",
                "tolerance": 1,
                "tolerance_paral": 1.2,
                "aya":'',
                }

        data = []

        response = requests.get(url, params=params)
        soup = BeautifulSoup(response.text, 'html.parser')
        tables = soup.find_all("table")

        tableIndex = 0
        for t in tables:
            headers = [th.get_text(strip=True) for th in t.find_all("td")[:5]]
            if headers == ["Planet", "Sign", "Degree", "House", "Motion"]:
                table=t
                break

            tableIndex =+ 1


        acsTable = tables[tableIndex + 1]
        acs = acsTable.find_all('tr')[0].find_all('td')
        acsSign = acs[1].get_text().split(' ')[0]
        acsDeg = acs[2].find('span').get_text()
        print(acsSign)
        print(acsDeg)


        
        rows = table.find_all('tr')[1:]
        
        for row in rows:
            cols = row.find_all('td')

            if len(cols) < 4:
                continue

            planet = cols[0].get_text().replace(':', '')
            sign = cols[1].get_text()
            degree = cols[2].find('span').get_text()
            house = cols[3].get_text()
            motion = cols[4].get_text()


            data.append({'planet':planet, 'sign':sign, 'degree':degree, 'house':house, 'motion':motion})

        return JsonResponse({'data':data ,'acs':[acsDeg, acsSign]})


    return render(request, 'pages/home.html')