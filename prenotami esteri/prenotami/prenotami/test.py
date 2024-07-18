from urllib.parse import quote,urlencode
import json

data = {
    "idCalendarioGiornaliero": "33128473",
    "selectedDay": "2024-07-24",
    "selectedHour": "10:01 - 10:30(1)"
}


print(data)

data = {
        "idCalendarioGiornaliero": data['idCalendarioGiornaliero'],
        "selectedDay": data['selectedDay'],
        "selectedHour": data['selectedHour']
    }
print(data)
data = {
        "idCalendarioGiornaliero": "33128473",
        "selectedDay": "2024-07-24",
        "selectedHour": "10:01 - 10:30(1)"
    }
print(data)
data = json.dumps(data)
print(data)