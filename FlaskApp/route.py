import requests
from math import sqrt

def coordinates(address):
    geocoder_request = f"http://geocode-maps.yandex.ru/1.x/" \
                        f"?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode=Казань, {address}&format=json"
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        return toponym["Point"]["pos"]
    else:
        return


def route_length(address1, address2):
    coordinates1, coordinates2 = coordinates(address1), coordinates(address2)
    if not coordinates1 or not coordinates2:
        return None
    else:
        coordinates1, coordinates2 = coordinates1.split(), coordinates2.split()
        return sqrt((float(coordinates1[0]) - float(coordinates2[0])) ** 2 +
                    (float(coordinates1[1]) - float(coordinates2[1])) ** 2)


print(route_length('Гаврилова, 2', "Чистопольская, 79"))
# вычислено: 0,0160200443 километра на единицу координат

def price_per_path(address1, address2):
    price = int((route_length(address1, address2) / 0.0160200443) * 100)
    return price


print(price_per_path('Гаврилова, 2', "Чистопольская, 79"))