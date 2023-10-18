import sys
import urllib.parse
import requests

BASE_URI = "https://weather.lewagon.com"

def search_city(query):
    cities = {'q': query, "limit": 5}
    query_string = urllib.parse.urlencode(cities)
    url = urllib.parse.urljoin(BASE_URI, f'/geo/1.0/direct?{query_string}')

    response = requests.get(url).json()

    if not response:
        print ("City not found.")
        return None

    if len(response) > 1:
        print("Multiple matches found. Please choose a city:")
        for i, city in enumerate(response, start=1):
            print (f"{i}. {city['name']}, {city['country']}")

        while True:
            try:
                choice = int(input("Enter the number of the city you meant: "))
                city = response[choice - 1]
                print(f"You selected: {city['name']}, {city['country']}")
                return city
            except (ValueError, IndexError):
                print ("Invalid input.")
    else:
        city = response[0]
        print (f"City: {city['name']}, Country: {city['country']}")
        return city

def weather_forecast(lat, lon):
    url = urllib.parse.urljoin(BASE_URI, "/data/2.5/forecast")
    forecasts = requests.get(url,
                             params={'lat': lat, 'lon': lon, 'units': 'metric'},
                             timeout=10).json()['list']

    return forecasts[::8]

def main():
    query = input("City?\n> ")
    city = search_city(query)

    if city:
        print (city)
        lat = city['lat']
        lon = city['lon']

        daily_forecasts = weather_forecast(lat, lon)
        for forecast in daily_forecasts:
            max_temp = round(forecast['main']['temp_max'])
            print (f"{forecast['dt_txt'][:10]}: {forecast['weather'][0]['main']} ({max_temp}°C)")

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
