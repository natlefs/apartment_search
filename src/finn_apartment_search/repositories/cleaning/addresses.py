from logging import PercentStyle
import string

from typing import Union
from dataclasses import dataclass
from urllib.parse import quote

"""
Addresses might not be found in a format that the Geonorge API can handle.
This module tries to clean them up.

A well-formatted address exists in one of these forms:
Veinavnet 38, Oslo
Vei med delt navn 214, Drammen
Annenvei 1, 1180 Oslo

A passable address might be:
Veinavn, Oslo
Veinavnet 38

A shitty address will be:
Veinavn
Oslo


The pattern that can be found from this is that:

A passable address contains:
* at least one alpha word with at least one alphanumeric word following it

In addition the well-formatted address will contain:
* a number (with possible letter on end) after the word and before the comma
* exactly one comma
* at least one alpha word on each side of the comma
"""

NORWEGIAN_ALPHA = string.ascii_lowercase + 'æøå'

@dataclass
class PerfectAddress:
    road_name: str
    house_number: int
    municipality: str

    def to_geodata_query(self) -> str:
        return f"{quote(self.road_name)}&nummer={str(self.house_number)}&poststed={quote(self.municipality.upper())}"

@dataclass
class SearchableAddress:
    address: str

    def to_geodata_query(self) -> str:
        return quote(self.address)
    

def transform_address(address) -> Union[SearchableAddress, PerfectAddress]:
    parts = address.split(',')
    if len(parts) == 1:
        return SearchableAddress(address)

    first = parts[0].lower()
    if is_norwegian_alnum(first) and not is_norwegian_alpha(first):
        # We probably have a "roadname 9129" case
        for i, char in enumerate(first):
            if char in string.digits:
                road_name = first[:i].strip()
                road_number = ''.join(c for c in first[i:].lower() if c in string.digits)
                break
            
    elif is_norwegian_alpha(first):
        # Means we are missing the road number
        road_name = first.strip()
        road_number= ''
    else:
        return SearchableAddress(address)

    if is_norwegian_alpha(parts[1].lower()):
        if road_name and road_number:
            return PerfectAddress(
                road_name=road_name,
                house_number=int(road_number),
                municipality=parts[1].strip()
            )
        formatted =  f"{road_name} {road_number}, " + parts[1].strip()
    else:
        formatted = f"{road_name} {road_number}"

    return SearchableAddress(formatted)

def is_norwegian_alnum(word):
    valid = string.digits + NORWEGIAN_ALPHA + ' '
    for c in word:
        if c not in valid:
            return False

    return True

def is_norwegian_alpha(word):
    valid = NORWEGIAN_ALPHA + ' '
    for c in word:
        if c not in valid:
            return False

    return True
