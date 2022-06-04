from importlib.abc import Traversable
import sys
import json

from dataclasses import asdict


from finn_apartment_search.utils import get_location, construct_searches, iter_urls
from finn_apartment_search.locations import WORK, OSLO_SOUTH, LILLESTROM, Location, StopPlace


from finn_apartment_search.repositories.finn.search_results import (
    get_finn_codes,
    get_page_tree,
    get_search_results
)
from finn_apartment_search.repositories.geodata.api import location_from_address
from finn_apartment_search.repositories.entur.api import get_itinerary
from finn_apartment_search.repositories.combined.filter_results import get_enriched_listings_simple, _SKOYEN_STASJON

from finn_apartment_search.repositories.finn.realestate import LettingsArticle

def _cli_loc():
    loc = get_location(input('enter url: '))
    print(loc)

def _cli_codes():
    url = 'https://www.finn.no/realestate/lettings/search.html?sort=PUBLISHED_DESC'
    root = get_page_tree(url)
    result = get_finn_codes(root, 3)
    print(result)

def _cli_searchurls():
    locations = [WORK, OSLO_SOUTH, LILLESTROM]
    for url in construct_searches(locations):
        print(url)


def _cli_demo(ceil=10):
    url = 'https://www.finn.no/realestate/lettings/search.html?area_from=70&facilities=23&lat=59.93831915210748&location=1.22030.20046&location=1.22030.20045&lon=10.576020983554486&no_of_bedrooms_from=3&price_to=25001&radius=10000&sort=AREA_DESC&stored-id=55060980'
    codes = get_finn_codes(url, ceil)

    articles = []
    for code, url in iter_urls(codes):
        articles.append(LettingsArticle.parse(url, code))


def _cli_actual(ceil_pages=20):
    url = "https://www.finn.no/realestate/lettings/search.html?area_from=75&facilities=23&lat=59.90309710055101&lon=10.782596234138992&no_of_bedrooms_from=2&price_to=25000&property_type=3&property_type=2&property_type=4&property_type=1&radius=100000&sort=PUBLISHED_DESC"
    places = get_enriched_listings_simple(url, _SKOYEN_STASJON, max_pages=20)
    places_as_dicts = [asdict(place) for place in places]
    places_as_dicts.sort(key=lambda a: a.get('score', 100))
    with open('full_results.json', 'w') as file:
        json.dump(places_as_dicts, file, indent=4)

def _cli_testsearchresult(ceil=20):
    """
    @dataclass
    class SearchResult:
        monthly_price: int
        size: int
        address: str
        title: str
        type: str
    """ 
    url = 'https://www.finn.no/realestate/lettings/search.html?area_from=85&location=1.22030.20046&location=1.22030.20045&location=1.20061.20533&location=1.20061.20507&location=1.20061.20531&no_of_bedrooms_from=2&price_to=25000&rent_from=202206&sort=AREA_DESC&stored-id=55360555'
    skoyen_stasjon = StopPlace("NSR:StopPlace:152", "Skøyen stasjon, Oslo")
    results = get_search_results(url)
    for result in results:
        article = location_from_address(result.address)
        alternatives, shortest = get_itinerary(article, skoyen_stasjon)


def _cli_testmanyresults(ceil=1):
    url = 'https://www.finn.no/realestate/lettings/search.html?area_from=85&no_of_bedrooms_from=2&price_to=25000&rent_from=202206&rent_from=202207&sort=AREA_DESC&stored-id=55360555'
    results = get_search_results(url, pages=1)
    with open("results.json", 'w') as file:
        results_as_dict = [asdict(r) for r in results]
        json.dump(results_as_dict, file, indent=4)


def _cli_testnew():
    url = 'https://www.finn.no/realestate/lettings/ad.html?finnkode=251761499'
    result = LettingsArticle.parse(url, 251761499)
    with open('single_article.json', 'w') as file:
        json.dump(asdict(result), file, indent=2)

def _cli_gql_test():
    start = Location(lat="59.8", lon="10.4")
    end = StopPlace("NSR:StopPlace:152", "Skøyen stasjon, Oslo")
    alternatives, shortest = get_itinerary(start, end)
    print(f"Amount of alternatives: {alternatives}\nShortest duration: {shortest / 60} minutes")


def _cli_testenriched():
    url = 'https://www.finn.no/realestate/lettings/search.html?area_from=85&no_of_bedrooms_from=2&page=7&price_to=25000&rent_from=202206&rent_from=202207&sort=AREA_DESC&stored-id=55360555'
    places = get_enriched_listings_simple(url, _SKOYEN_STASJON, max_pages=1)
    places_as_dicts = [asdict(place) for place in places]
    with open('enriched_results.json', 'w') as file:
        json.dump(places_as_dicts, file)


CLI_FUNCS = {k[5:]: v for k, v in locals().items() if k.startswith('_cli_')}


def main():
    """argparse is too much boilerplate"""
    func = print
    try:
        func = CLI_FUNCS[sys.argv[1]]
        func()
    except (KeyError, IndexError):
        print('The valid parameters are: ' + ', '.join(CLI_FUNCS.keys()))
        raise
    

if __name__ == '__main__':
    main()
