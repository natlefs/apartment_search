from dataclasses import dataclass
from lxml.html import Element
from typing import Optional, List
from types import LambdaType
from abc import ABC


@dataclass
class FindingStrategy:
    xpath: Optional[str] = None
    css_selector: Optional[str] = None

    def find_in(self, root) -> List[Element]:
        """Finds an HTML element in a lxml HTML tree"""
        if self.css_selector is not None:
            return root.cssselect(self.css_selector)

        if self.xpath is not None:
            return root.xpath(self.xpath)

    def __post_init__(self):
        if self.xpath is None and self.css_selector is None:
            raise ValueError('A FindingStrategy must have a search'
                             + 'parameter(xpath/css_selector) provided')

@dataclass
class SingleElementValueFinder(ABC):
    strategies: list[FindingStrategy]
    extract_value: Optional[LambdaType] = None
    transform_result: Optional[LambdaType] = None

    def get(self, root):
        """Gets the value of an element"""
        element = self.__find_one_value(root)
        if element is None:
            return None

        value = self._extract_value(element)

        if self.transform_result is not None:
            return self.transform_result(value)

        return value
        

    def __find_one_value(self, root) -> Element:
        for strategy in self.strategies:
            result = strategy.find_in(root)
            if len(result) >= 1:
                return result[0]

        return None

    def _extract_value(self, element) -> str:
        """Gets the value of given element, potentially transformed to make sense"""
        if self.extract_value is None:
            return element.text
        else:
            return self.extract_value(element)

    @classmethod
    def new(cls, xpath: str=None, css_selector: str=None):
        strats = []
        if xpath is not None:
            strats.append(FindingStrategy(xpath=xpath))
        if css_selector is not None:
            strats.append(FindingStrategy(css_selector=css_selector))
        return cls(strats)

@dataclass
class MultiElementValueFinder(SingleElementValueFinder):
    """Finds a set of elements and extracts their value"""
    strategies: list[FindingStrategy]
    extract_value: Optional[LambdaType] = None
    transform_result: Optional[LambdaType] = None

    def get(self, root, ceil=None):
        """
        Gets the value of a set of elements,
        optionally limiting the amount returned.
        Returns them in a list
        """
        elements = self.__find_values(root)
        if ceil is None:
            result = [self._extract_value(e) for e in elements]
        else:
            result = [self._extract_value(e) for i, e in enumerate(elements) if i <= ceil]
        
        if self.transform_result is not None:
            return self.transform_result(result)

        return result

    def __find_values(self, root) -> List[Element]:
        for strategy in self.strategies:
            result = strategy.find_in(root)
            if len(result) > 0:
                return result
        return []
