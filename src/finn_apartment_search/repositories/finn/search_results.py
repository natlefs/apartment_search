import re
import time
from tokenize import Single

from lxml import html
from urllib.request import urlopen
from dataclasses import dataclass
from typing import List

from scraping.element_value_finder import (
    SingleElementValueFinder,
    MultiElementValueFinder,
    FindingStrategy
)

from scraping.formatting import (
    to_numeric
)

_whitespace = re.compile(r'\s+')

@dataclass
class SearchResult:
    finn_code: int
    url: str
    monthly_price: int
    size: int
    address: str
    title: str
    type: str

search_page_is_empty = SingleElementValueFinder(
    [FindingStrategy(css_selector="div.panel h2.u-t3")],
    extract_value=lambda e: e.text.startswith('Ingen treff')
).get

def filter_and_extract_finn_code(elements):
    result = []
    for article in elements:
        try:
            if len(article.cssselect("span span.status")) == 0:
                link = article.cssselect("a")[0]
                result.append(link.attrib['id'])
        except Exception as ex:
            continue
    return result


get_finn_codes = MultiElementValueFinder(
    [FindingStrategy(css_selector="article[class]")],
    extract_value=lambda e: e,
    transform_result=filter_and_extract_finn_code
).get

def _parse_search_result(elements):
    result = []
    for article in elements:
        try:
            if len(article.cssselect("span span.status")) == 0:
                link = article.cssselect("a")[0]
                _id = link.attrib['id']
                title, url, finn_code = SingleElementValueFinder(
                    [FindingStrategy(css_selector="h2 a")],
                    extract_value=lambda e: (e.text, e.get('href'), e.get('id'))
                ).get(article)
                type = SingleElementValueFinder.new(css_selector="div.pt-6 div.text-12").get(article)
                address = SingleElementValueFinder.new(css_selector="div.pt-6 div span.text-14").get(article)
                size = SingleElementValueFinder([FindingStrategy(xpath="div[3]/div[3]/span[1]")], extract_value=lambda e: to_numeric(e.text)).get(article)
                monthly_price = SingleElementValueFinder([FindingStrategy(xpath="div[3]/div[3]/span[2]")], extract_value=lambda e: int(re.sub(_whitespace, '', e.text))).get(article)
                result.append(SearchResult(
                    finn_code=finn_code,
                    url=url,
                    monthly_price=monthly_price,
                    size=size,
                    address=address,
                    title=title,
                    type=type
                ))
        except Exception as ex:
            print(ex)
    return result


_parse_search_results = MultiElementValueFinder(
    [FindingStrategy(css_selector="article[class]")],
    extract_value=lambda e: e,
    transform_result=_parse_search_result
).get


def get_search_results(url, pages=50, wait=0.3) -> List[SearchResult]:
    results = []
    host = url.split('?')[0]

    for _ in range(pages):
        time.sleep(wait)

        data = urlopen(url)
        root = html.parse(data).getroot()
        results += _parse_search_results(root)

        query = get_next_page_query(root)
        if query is None:
            break
        url = host + query

    return results


get_next_page_query = SingleElementValueFinder(
    [FindingStrategy(css_selector="nav.pagination > a[rel=next]")],
    extract_value=lambda e: e.get('href')
).get

def get_page_tree(url):
    data = urlopen(url)
    return html.parse(data).getroot()
