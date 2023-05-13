from abc import ABC, abstractmethod
from xml.etree import ElementTree as Et


class XMLAble(ABC):
    @abstractmethod
    def to_xml_element(self) -> Et.Element:
        pass

    @staticmethod
    @abstractmethod
    def parse_from_xml_element(element):
        pass
