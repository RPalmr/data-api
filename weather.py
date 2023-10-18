# pylint: disable=missing-module-docstring

import sys
import urllib.parse
import requests

BASE_URI = "https://weather.lewagon.com"

def search_city(query):
    '''
    Look for a given city. If multiple options are returned, choose the first one.
    Return one city (or None)
    '''
    cities = {'q': query, "limit": 5}
    query_string = urllib.parse.urlencode(cities)
    endpoint = '/geo/1.0/direct'
    url = urllib.parse.urljoin(BASE_URI, endpoint + '?' + query_string)

    response = requests.get(url).json()

    if not response:
        print("City not found.")
        return None

    # Choose the first city if multiple are found
    city = response[0]
    print(f"{city['name']}: ({city['lat']}, {city['lon']})")
    return city

def weather_forecast(lat, lon):
    '''Return a 5-day weather forecast for the city, given its latitude and longitude.'''

def main():
    '''Ask user for a city and display weather forecast'''
    query = input("City?\n> ")
    city = search_city(query)

    # TODO: Display weather forecast for a given city
    pass  # YOUR CODE HERE

if __name__ == '__main__':
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print('\nGoodbye!')
        sys.exit(0)
