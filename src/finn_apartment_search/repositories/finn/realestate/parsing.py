import re
from urllib.parse import urlparse, parse_qs
from locations import Location
from lxml import etree

from scraping.element_value_finder import (
    SingleElementValueFinder,
    MultiElementValueFinder,
    FindingStrategy
)

def _parse_finn_map_location(element):
    url = element.attrib['src']
    parsed = urlparse(url)
    params = parse_qs(parsed.query)
    lat, lon = params['lat'][0], params['lng'][0]
    return Location(lat=lat, lon=lon)

getMapLocation = SingleElementValueFinder(
    [FindingStrategy(css_selector="div.panel a img[alt='Kart']")],
    extract_value=_parse_finn_map_location
).get

getAddress = SingleElementValueFinder.new(css_selector="p.u-caption").get

getDescription = MultiElementValueFinder(
    [FindingStrategy(css_selector="div#collapsableTextContent p")],
    extract_value=lambda root: etree.tostring(root).decode('utf-8', 'ignore').strip(),
    transform_result=lambda results: '<br />'.join([r for r in results if r])
).get

getFacilities = MultiElementValueFinder.new(css_selector="ul.list--bullets li").get

def default_formatter(element, header=None):
    """Removes artifacts in some preconfigured fields"""
    if header == 'Primærrom':
        return fix_number(element, 2)
    elif header == 'Etasje':
        return fix_number(element, 1)
    elif header == 'Soverom':
        return int(element.text)
    return element.text.strip()

def to_numeric(text):
    if text[-2:] == 'm²':
        return int(text[-3:])
    elif text[-2] == 'kr':
        return int(text[-3:])

def fix_number(element, postfix_len=2):
    """Strips off whitespace, configured postfix characters and converts number to int"""
    nums = element.text.strip()[:-postfix_len]
    nums = re.sub(r'\s', '', nums)
    return int(nums)


def dl_to_dict(element, formatter=default_formatter):
    """Transforms a HTML dl element into a dict"""
    result = {}
    header = ''
    for sub in element.getchildren():
        if sub.tag == 'dt':
            header = sub.text.strip()
        else:
            result[header] = formatter(sub, header)
    return result

def joindict(x):
    """Combines the keys and values in a list of dicts into a single dict"""
    result = {}
    for dct in x:
        for k, v in dct.items():
            result[k] = v
    return result

getDetails = MultiElementValueFinder(
    [FindingStrategy(css_selector="dl.definition-list")],
    extract_value=dl_to_dict,
    transform_result=joindict
).get

getImageCount = MultiElementValueFinder(
    [FindingStrategy(css_selector="div[data-carousel-container] a")],
    extract_value=lambda x: 1,
    transform_result=sum
).get

getPrice = SingleElementValueFinder(
    [FindingStrategy(css_selector="div.panel > span.u-t3")],
    extract_value=fix_number
).get

getTitle = SingleElementValueFinder.new(css_selector="h1.u-t2").get