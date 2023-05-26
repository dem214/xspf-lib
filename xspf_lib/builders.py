__all__ = ["build_playlist", "build_track"]

from collections.abc import Iterable
from typing import TYPE_CHECKING, Union
from xml.etree import ElementTree as Et

from .base import XMLAble
from .constants import XML_NAMESPACE
from .utils import quote

if TYPE_CHECKING:
    from .elements import Playlist, Track


class _XMLBuilder:
    def __init__(self):
        self.entity: Union["Track", "Playlist", None] = None

    def build_track(self, track: "Track"):
        self.entity = track
        self.xml_element = Et.Element("track")

        self.add_locations()
        self.add_identifiers()
        self.add_title()
        self.add_creator()
        self.add_annotation()
        self.add_info()
        self.add_image()
        self.add_album()
        self.add_track_num()
        self.add_duration()
        self.add_links()
        self.add_metas()
        self.add_extensions()

        return self.xml_element

    def build_playlist(self, playlist: "Playlist") -> Et.Element:
        self.entity = playlist
        self.xml_element = Et.Element(
            "playlist", {"version": "1", "xmlns": XML_NAMESPACE["xspf"]}
        )

        self.add_title()
        self.add_creator()
        self.add_annotation()
        self.add_info()
        self.add_location()
        self.add_identifier()
        self.add_image()
        self.add_date()
        self.add_license()
        self.add_attribution()
        self.add_links()
        self.add_metas()
        self.add_extensions()
        self.add_tracklist()

        return self.xml_element

    def add_locations(self):
        if self.entity.location is not None:
            for loc in self.entity.location:
                Et.SubElement(self.xml_element, "location").text = str(quote(loc))

    def add_identifiers(self):
        if self.entity.identifier is not None:
            for id in self.entity.identifier:
                Et.SubElement(self.xml_element, "identifier").text = str(id)

    def add_license(self):
        self.add_simple_subelement("license")

    def add_attribution(self):
        if len(self.entity.attribution) > 0:
            attribution = Et.SubElement(self.xml_element, "attribution")
            for attr in self.entity.attribution[0:9]:
                if attr.location is not None:
                    Et.SubElement(attribution, "location").text = attr.location
                if attr.identifier is not None:
                    Et.SubElement(attribution, "identifier").text = attr.identifier

    def add_tracklist(self):
        Et.SubElement(self.xml_element, "trackList").extend(
            track.to_xml_element() for track in self.entity.trackList
        )

    def add_title(self):
        self.add_simple_subelement("title")

    def add_creator(self):
        self.add_simple_subelement("creator")

    def add_annotation(self):
        self.add_simple_subelement("annotation")

    def add_info(self):
        self.add_simple_subelement("info")

    def add_image(self):
        self.add_simple_subelement("image")

    def add_album(self):
        self.add_simple_subelement("album")

    def add_track_num(self):
        self.add_simple_subelement("trackNum")

    def add_duration(self):
        self.add_simple_subelement("duration")

    def add_links(self):
        self.add_iterable_parameter("link")

    def add_metas(self):
        self.add_iterable_parameter("meta")

    def add_extensions(self):
        self.add_iterable_parameter("extension")

    def add_location(self):
        self.add_simple_subelement("location")

    def add_identifier(self):
        self.add_simple_subelement("identifier")

    def add_date(self):
        Et.SubElement(self.xml_element, "date").text = self.entity.date.isoformat()

    def add_simple_subelement(self, parameter_name: str):
        parameter = getattr(self.entity, parameter_name, None)
        if parameter is not None:
            Et.SubElement(self.xml_element, parameter_name).text = str(parameter)

    def add_iterable_parameter(self, parameter_name: str):
        parameter_iter: Iterable[XMLAble] = getattr(self.entity, parameter_name)
        self.xml_element.extend(
            parameter.to_xml_element() for parameter in parameter_iter
        )


def build_track(track: "Track") -> Et.Element:
    return _XMLBuilder().build_track(track)


def build_playlist(playlist: "Playlist") -> Et.Element:
    return _XMLBuilder().build_playlist(playlist)
