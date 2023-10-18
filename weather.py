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
        print("City not found.")
        return None

    if len(response) > 1:
        print("Multiple matches found. Please choose a city:")
        for i, city in enumerate(response, start=1):
            print(f"{i}. {city['name']}, {city['country']}")

        while True:
            try:
                choice = int(input("Enter the number of the city you meant: "))
                city = response[choice - 1]
                print(f"You selected: {city['name']}, {city['country']}")
                return city
            except (ValueError, IndexError):
                print("Invalid input.")
    else:
        city = response[0]
        print(f"City: {city['name']}, Country: {city['country']}")
        return city

def weather_forecast(lat, lon):
    endpoint = f'/data/2.5/forecast?lat={lat}&lon={lon}'
    url = BASE_URI + endpoint
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'list' in data:
            for forecast in data['list'][:5]:
                date_time = forecast['dt_txt'].split()
                temperature = forecast['main']['temp'] - 273.15
                weather_description = forecast['weather'][0]['description']
                print(f"{date_time[0]}, {weather_description}, ({temperature:.2f}°C),")
        else:
            print("Data is incomplete or missing.")
    else:
        print(f"Error: {response.status_code} - {response.text}")

def main():
    query = input("City?\n> ")
    city = search_city(query)

    if city:
        lat = city['lat']
        lon = city['lon']
        weather_forecast(lat, lon)

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
