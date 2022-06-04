import json
from dataclasses import dataclass
from email.headerregistry import Address
from re import S
from urllib import parse
from locations import Location, StopPlace, WORK
from typing import Union




class SearchConstructor:
    ROOT = 'https://www.finn.no/realestate/homes/search.html?'
    POSTFIX = '&sort=PUBLISHED_DESC'

    def __init__(self, location=WORK):
        self.latitude = location.lat
        self.longitude = location.lon
        self.radius = 8000
        self.max_monthly_cost = 4000
        self.bedrooms = 1
        self.total_price = 4800000

    def __call__(self, location=None):
        if location is not None:
            self.latitude = location.lat
            self.longitude = location.lon
        return self.construct()

    def construct(self):
        return self.ROOT + f'lat={self.latitude}&lon={self.longitude}&radius={self.radius}&no_of_bedrooms={1}&price_collective_to={self.total_price}&rent_to={self.max_monthly_cost}{self.POSTFIX}'


def construct_searches(locations, constructor=None):
    """From a set of lat/long positions generate finn.no searches"""
    if constructor is None:
        constructor = SearchConstructor()
    for location in locations:
        yield constructor(location)


def get_location(url):
    """
    Parses url of of different maps to give find lat/long positiion
    https://www.google.no/maps/place/Gamle+Oslo,+Oslo/@59.8724943,10.7508296,13z/data=!4m5!3m4!1s0x46416e55ec405b67:0x10d50d66ed90d75c!8m2!3d59.9067752!4d10.7622822?hl=no
    https://maptiles.finncdn.no/staticmap?lat=59.89571&lng=10.814899&zoom=14&size=800x400&maptype=norwayVector&showPin=true
    into a latitude and longitude position.
    Returns that pair as a Location
    """
    try:
        if 'google' in url:
            lat, lon = url.split('@')[1].split(',')[:2]
        elif 'finncdn' in url:
            components = parse.urlparse(url)
            queries = parse.parse_qs(components.query)
            lat, lon = queries['lat'][0], queries['lng'][0]
        return Location(lat, lon)
    except:
        print('Error: invalid url')


def iter_urls(finn_codes, category='lettings'):
    for code in finn_codes:
        yield (code, get_url(code, category))

def get_url(finn_code, category='realestate/homes'):
    if category == 'lettings':
        return f'https://www.finn.no/realestate/lettings/ad.html?finnkode={finn_code}'
    return f'https://www.finn.no/{category}/ad.html?finnkode={finn_code}'

