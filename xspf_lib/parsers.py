__all__ = ["TrackBaseParser", "PlaylistBaseParser"]

from datetime import datetime
from typing import Any, Generic, Optional, TypeVar, Union
from urllib import parse as urlparse
from xml.etree import ElementTree as Et

from .constants import XML_NAMESPACE
from .elements import Attribution, Extension, Link, Meta, Playlist, Track
from .utils import urify

T = TypeVar("T", bound=Union[Track, Playlist])


class BaseParser(Generic[T]):
    parsing_entity: T

    def __init__(self, xml_element: Et.Element):
        self.xml_element = xml_element

    @staticmethod
    def check_element_nonleaf_content(element: Et.Element) -> None:
        if element.text is not None and not element.text.isspace():
            raise TypeError(
                f"Element <{element.tag}> nonleaf "
                "content is not allowed.\n"
                f"| Got `{element.text}`."
            )

    def insert_title(self) -> None:
        title = self.get_xml_leaf_parameter_value("title")
        self.insert_parameter_if_not_null("title", title)

    def insert_creator(self) -> None:
        creator = self.get_xml_leaf_parameter_value("creator")
        self.insert_parameter_if_not_null("creator", creator)

    def insert_annotation(self) -> None:
        annotation = self.get_xml_leaf_parameter_value("annotation")
        self.insert_parameter_if_not_null("annotation", annotation)

    def insert_info(self):
        info = self.get_xml_leaf_parameter_uri_value("info")
        self.insert_parameter_if_not_null("info", info)

    def insert_image(self) -> None:
        image = self.get_xml_leaf_parameter_uri_value("image")
        self.insert_parameter_if_not_null("image", image)

    def insert_links(self) -> None:
        self.parsing_entity.link.extend(
            Link.parse_from_xml_element(link)
            for link in self.xml_element.findall("xspf:link", XML_NAMESPACE)
        )

    def insert_metas(self) -> None:
        self.parsing_entity.meta.extend(
            Meta.parse_from_xml_element(meta)
            for meta in self.xml_element.findall("xspf:meta", XML_NAMESPACE)
        )

    def insert_extensions(self) -> None:
        self.parsing_entity.extension.extend(
            Extension.parse_from_xml_element(extension)
            for extension in self.xml_element.findall("xspf:extension", XML_NAMESPACE)
        )

    def insert_parameter_if_not_null(
        self, parameter_name: str, parameter_value: Any
    ) -> None:
        if parameter_value is not None:
            self.parsing_entity.__setattr__(parameter_name, parameter_value)

    def get_xml_leaf_parameter_value(self, parameter_name: str) -> Optional[str]:
        return self._get_xml_leaf_parameter_value_with_urify(
            parameter_name, need_urify=False
        )

    def get_xml_leaf_parameter_int_value(self, parameter_name: str) -> Optional[int]:
        value = self.get_xml_leaf_parameter_value(parameter_name)
        return int(value) if value is not None else None

    def get_xml_leaf_parameter_uri_value(self, parameter_name: str) -> Optional[str]:
        return self._get_xml_leaf_parameter_value_with_urify(
            parameter_name, need_urify=True
        )

    def _get_xml_leaf_parameter_value_with_urify(
        self, parameter_name: str, need_urify: bool = False
    ) -> Optional[str]:
        self.check_single_element_in_root(parameter_name)
        parameter = self.xml_element.find("xspf:" + parameter_name, XML_NAMESPACE)
        if parameter is None:
            return None
        self.check_inserted_markup(parameter)
        self.check_forbidden_element_attributes(parameter)
        ret_text = parameter.text
        if ret_text is None:
            return None
        return ret_text if not need_urify else urify(ret_text)

    def check_single_element_in_root(self, element_name: str) -> None:
        if len(self.xml_element.findall("xspf:" + element_name, XML_NAMESPACE)) > 1:
            raise TypeError(
                f"Got too many `{element_name}` elements in "
                "playlist.\n"
                f"{Et.tostring(self.xml_element)}"
            )

    @staticmethod
    def check_inserted_markup(element) -> None:
        if len(list(element)) > 0:
            raise ValueError(
                "Got nested elements in expected text. "
                "Probably, this is unexpected HTML "
                "insertion.\n"
                f"{Et.tostring(element)}"
            )

    @staticmethod
    def check_forbidden_element_attributes(element) -> None:
        if len(element.attrib) > 0 and element.keys() != [
            "{http://www.w3.org/XML/1998/namespace}base"
        ]:
            raise TypeError(
                "Element contains forbidden attribute "
                f"{element.attrib}.\n"
                f"{Et.tostring(element)}"
            )


class TrackBaseParser(BaseParser[Track]):
    def __init__(self, xml_element: Et.Element):
        super().__init__(xml_element)
        self.parsing_entity = Track()

    def parse(self) -> Track:
        self.check_all_track_element()
        self.insert_all_parameters()
        return self.parsing_entity

    def check_all_track_element(self) -> None:
        self.check_root_name_and_namespace()
        self.check_track_nonleaf_content()

    def check_root_name_and_namespace(self) -> None:
        if self.xml_element.tag != f'{{{XML_NAMESPACE["xspf"]}}}track':
            raise TypeError(
                "Track element not contain 'track' tag ",
                "or namespace setted wrong",
            )

    def check_track_nonleaf_content(self) -> None:
        self.__class__.check_element_nonleaf_content(self.xml_element)

    def insert_all_parameters(self):
        self.insert_locations()
        self.insert_identifiers()
        self.insert_title()
        self.insert_creator()
        self.insert_annotation()
        self.insert_info()
        self.insert_image()
        self.insert_album()
        self.insert_track_num()
        self.insert_duration()
        self.insert_links()
        self.insert_metas()
        self.insert_extensions()

    def insert_locations(self) -> None:
        locations = self.xml_element.findall("xspf:location", XML_NAMESPACE)
        if len(locations) > 0:
            self.parsing_entity.location = [
                urlparse.unquote(urify(location.text.strip()))
                for location in locations
                if location.text is not None
            ]

    def insert_identifiers(self) -> None:
        identifiers = self.xml_element.findall("xspf:identifier", XML_NAMESPACE)
        if len(identifiers) > 0:
            self.parsing_entity.identifier = [
                urlparse.unquote(urify(identifier.text.strip()))
                for identifier in identifiers
                if identifier.text is not None
            ]

    def insert_album(self) -> None:
        album = self.get_xml_leaf_parameter_value("album")
        self.insert_parameter_if_not_null("album", album)

    def insert_track_num(self) -> None:
        track_num = self.get_xml_leaf_parameter_int_value("trackNum")
        self.insert_parameter_if_not_null("trackNum", track_num)

    def insert_duration(self) -> None:
        duration = self.get_xml_leaf_parameter_int_value("duration")
        self.insert_parameter_if_not_null("duration", duration)


class PlaylistBaseParser(BaseParser[Playlist]):
    def __init__(self, xml_element: Et.Element):
        super().__init__(xml_element)
        self.parsing_entity = Playlist()

    def parse(self) -> Playlist:
        self.check_all_in_root_element()
        self.insert_all_parameters()
        return self.parsing_entity

    def check_all_in_root_element(self) -> None:
        self.check_namespace_is_exist()
        self.check_for_right_namespace_string()
        self.check_root_tag_name()
        self.check_version_attribute_is_exist()
        self.check_forbidden_root_attributes()
        self.check_value_of_version()
        self.check_root_nonleaf_content()

    def check_namespace_is_exist(self) -> None:
        if not self.xml_element.tag[0] == "{":
            raise TypeError(
                "Playlist namespace attribute is missing.\n"
                f"{Et.tostring(self.xml_element)}"
            )

    def check_for_right_namespace_string(self) -> None:
        if not self.xml_element.tag.startswith(
            "".join(["{", XML_NAMESPACE["xspf"], "}"])
        ):
            wrong_namespace = self.xml_element.tag.split("}")[0].lstrip("{")
            raise ValueError(
                "Namespace is wrong string.\n"
                f"| Expected `{XML_NAMESPACE['xspf']}`.\n"
                f"| Got `{wrong_namespace}`."
            )

    def check_root_tag_name(self) -> None:
        if self.xml_element.tag != "".join(["{", XML_NAMESPACE["xspf"], "}playlist"]):
            raise ValueError(
                "Root tag name is not correct.\n"
                "| Expected: `playlist`.\n"
                f"| Got: `{self.xml_element.tag.split('}')[1]}`"
            )

    def check_version_attribute_is_exist(self) -> None:
        # Version attribute check.
        if "version" not in self.xml_element.keys():
            raise TypeError("version attribute of playlist is missing.")

    def check_forbidden_root_attributes(self) -> None:
        root_attribs = self.xml_element.keys()
        if not (
            root_attribs == ["version"]
            or root_attribs == ["version", "{http://www.w3.org/XML/1998/namespace}base"]
        ):
            forbidden_attributes = list(root_attribs)
            try:
                forbidden_attributes.remove("version")
            except ValueError:
                pass
            try:
                forbidden_attributes.remove(
                    "{http://www.w3.org/XML/1998/namespace}base"
                )
            except ValueError:
                pass
            raise TypeError(
                "<playlist> element contains forbidden elements.\n"
                f"{forbidden_attributes}"
            )

    def check_value_of_version(self) -> None:
        version = int(self.xml_element.get("version", "0"))
        # 0 version not implemented
        if version == 0:
            raise ValueError(
                "XSPF version 0 is not maintained, " "switch to version 1."
            )
        # Another version than 1 not accepted.
        elif version != 1:
            raise ValueError(
                "The 'version' attribute must be 1.\n"
                f"Your playlist version setted to {version}.\n"
                "See https://xspf.org/xspf-v1.html#rfc.section.4.1.1.1.2"
            )

    def check_root_nonleaf_content(self) -> None:
        self.__class__.check_element_nonleaf_content(self.xml_element)

    def insert_all_parameters(self) -> None:
        self.insert_title()
        self.insert_creator()
        self.insert_annotation()
        self.insert_info()
        self.insert_location()
        self.insert_identifier()
        self.insert_image()
        self.insert_license()
        self.insert_date()
        self.insert_attributions()
        self.insert_links()
        self.insert_metas()
        self.insert_extensions()
        self.insert_tracklist()

    def insert_location(self) -> None:
        location = self.get_xml_leaf_parameter_uri_value("location")
        self.insert_parameter_if_not_null("location", location)

    def insert_identifier(self) -> None:
        identifier = self.get_xml_leaf_parameter_uri_value("identifier")
        self.insert_parameter_if_not_null("identifier", identifier)

    def insert_license(self) -> None:
        _license = self.get_xml_leaf_parameter_uri_value("license")
        self.insert_parameter_if_not_null("license", _license)

    def insert_date(self) -> None:
        date_string = self.get_xml_leaf_parameter_value("date")
        if date_string is not None:
            date_string = date_string.strip()
            date_object = datetime.fromisoformat(date_string)
            self.insert_parameter_if_not_null("date", date_object)

    def insert_attributions(self) -> None:
        self.check_single_element_in_root("attribution")
        attribution = self.xml_element.find("xspf:attribution", XML_NAMESPACE)
        if attribution is not None:
            self.__class__.check_element_nonleaf_content(attribution)
            self.parsing_entity.attribution.extend(
                Attribution().parse_from_xml_element(attr) for attr in attribution
            )

    def insert_tracklist(self) -> None:
        self.check_tracklist_is_only_one()
        tracklist = self.xml_element.find("xspf:trackList", XML_NAMESPACE)
        if tracklist is None:
            return
        self.check_element_nonleaf_content(tracklist)
        self.parsing_entity.trackList.extend(
            Track.parse_from_xml_element(track) for track in tracklist
        )

    def check_tracklist_is_only_one(self) -> None:
        self.check_single_element_in_root("trackList")
        track_list = self.xml_element.find("xspf:trackList", XML_NAMESPACE)
        if track_list is None:
            raise TypeError("trackList element not founded.")
