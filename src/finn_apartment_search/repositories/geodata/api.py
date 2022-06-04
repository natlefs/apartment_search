from typing import List
from dataclasses import dataclass

import requests

from finn_apartment_search.locations import Location
from finn_apartment_search.repositories.cleaning.addresses import transform_address

HOST = 'https://ws.geonorge.no/adresser/v1/'
# Docs for API can be found on host URL

@dataclass
class DetailedLocation:
    road: str
    road_number: int
    zip_code: str
    units: List[str]
    municipality: str
    location: Location


def location_from_address(address) -> DetailedLocation:
    search_string = transform_address(address).to_geodata_query()
    response = requests.get(f"{HOST}sok?sok={search_string}&sokemodus=AND")

    body = response.json()
    count_results = body['metadata']['totaltAntallTreff']
    if count_results >= 1:
        result = body['adresser'][0]
        position = result['representasjonspunkt']
        return DetailedLocation(
            road=result.get('adressenavn'),
            road_number=result.get('nummer'),
            zip_code=result.get('postnummer'),
            units=result.get('bruksenhetsnummer'),
            municipality=result.get('kommunenavn'),
            location=Location(lat=position['lat'], lon=position['lon'])
        )
