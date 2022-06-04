import time
import random
from dataclasses import dataclass
from typing import Iterator, Union

from locations import StopPlace, Location
from repositories.finn.search_results import get_search_results, SearchResult
from repositories.geodata.api import location_from_address, DetailedLocation
from repositories.entur.api import get_itinerary, ItinerarySearchParameters

_URL = 'https://www.finn.no/realestate/lettings/search.html?area_from=85&location=1.22030.20046&location=1.22030.20045&location=1.20061.20533&location=1.20061.20507&location=1.20061.20531&no_of_bedrooms_from=2&price_to=25000&rent_from=202206&sort=AREA_DESC&stored-id=55360555'
_SKOYEN_STASJON = StopPlace("NSR:StopPlace:152", "Skøyen stasjon, Oslo")

class ResultsFilter:
    pass

@dataclass
class EnrichedListing:
    score: int
    search_result: SearchResult
    detailed_location: DetailedLocation
    shortest_duration: int

def get_enriched_listings_simple(
            url,
            itinerary_destination: Union[Location, StopPlace],
            max_pages=2
    ) -> Iterator[EnrichedListing]:
    
    
    results = get_search_results(url, pages=max_pages)

    for result in results:
        print(result.title, result.size, result.monthly_price)
        if "bofellesskap" in result.title:
            continue

        time.sleep(random.randrange(3, 8) / 10)
        detailed_location = location_from_address(result.address)
        if detailed_location is not None:
            location = detailed_location.location
            entur_params = ItinerarySearchParameters(location, itinerary_destination, 3)
            shortest = get_itinerary(entur_params)
        else:
            print(f"Did not find listing with address: {result.address}")
            shortest = None

        if result:
            yield EnrichedListing(
                score=score(result.monthly_price, result.size, shortest),
                search_result=result,
                detailed_location=detailed_location,
                shortest_duration=shortest
            )

def score(price, size, travel_distance):
    if price and size and travel_distance:
        if travel_distance > 3600:
            return price/20000 + (100*2)/size + travel_distance*3/1800
        # Score where the smallest is best, typically within 3-10
        return price/20000 + (100*2)/size + travel_distance*2/1800


    return 100
