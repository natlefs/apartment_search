import re
from dataclasses import dataclass
from typing import Union, Tuple, List
from datetime import date
from locations import Location
from repositories.finn.realestate import parsing
from urllib.request import urlopen
from lxml import html

from repositories.finn.article import Article


@dataclass
class LettingsArticle(Article):
    monthly_price: int
    living_area: int
    bedrooms: int
    storey: int

    address: str
    location: Location

    count_pictures: int
    renting_period: Union[date, Tuple[date, date]]
    facilities: List[str]
    description: str

    @classmethod
    def parse(cls, url, finn_id) -> Article:
        data = urlopen(url)
        root = html.parse(data).getroot()
        details = parsing.getDetails(root)
 
        return LettingsArticle(
            finn_id=finn_id,
            title=parsing.getTitle(root),
            renting_period=details.get('Leieperiode'),
            monthly_price=parsing.getPrice(root),
            living_area=details.get('Primærrom'),
            bedrooms=details.get('Soverom'),
            storey=details.get('Etasje'),
            address=parsing.getAddress(root),
            location=parsing.getMapLocation(root),
            count_pictures=parsing.getImageCount(root),
            facilities=parsing.getFacilities(root),
            description=parsing.getDescription(root)
        )

    @staticmethod
    def testIsWorking(source, expected) -> bool:
        raise NotImplementedError()

    @staticmethod
    def score(scoring_method) -> int:
        raise NotImplementedError()

@dataclass
class RealEstateArticle(Article):
    total_price: int
    recommended_price: int
    costs: int
    monthly_costs: int

    living_area: int
    bedrooms: int
    storey: int

    address: str
    location: Location

    count_pictures: int
    renting_period: Union[date, Tuple[date, date]]
    facilities: List[str]
    description: str


    @classmethod
    def parse(cls, url) -> Article:
        pass

    @staticmethod
    def testIsWorking(source, expected) -> bool:
        raise NotImplementedError()

    @staticmethod
    def score(scoring_method) -> int:
        raise NotImplementedError()
