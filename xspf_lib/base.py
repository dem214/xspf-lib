__all__ = ["XMLAble"]

from abc import ABC, abstractmethod
from xml.etree import ElementTree as Et


class XMLAble(ABC):
    @abstractmethod
    def to_xml_element(self) -> Et.Element:
        """Convert data model to :py:class:`xml.etree.ElementTree.Element`"""

    @staticmethod
    @abstractmethod
    def parse_from_xml_element(element: Et.Element):
        """Parse :py:class:`xml.etree.ElementTree.Element` to data model"""
