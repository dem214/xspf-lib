"""Module helps to work with xspf playlists."""

import xml.etree.ElementTree as ET
from typing import Iterable, Optional, Union, Dict
from datetime import datetime, timezone
from collections import UserList
import urllib.parse as urlparse
from dataclasses import dataclass

__all__ = ["Playlist", "Track", "Extension", "Link", "Meta", "URI",
           "Attribution"]

URI = str
NS = {'xspf': "http://xspf.org/ns/0/"}

ET.register_namespace('xspf', NS['xspf'])


def quote(value: str) -> str:
    return urlparse.quote(value, safe='/:')


class Extension():
    """Class for XML extensions of XSPF playlists and tracks."""

    __slots__ = ['application', 'extra_attrib', 'content']

    def __init__(self, application: URI,
                 extra_attrib: Dict[str, str] = {},
                 content: Iterable[ET.Element] = []) -> None:
        """Create Extension for xspf_lib.Track and xspf_lib.Playlist.

        Extension must have attribute `application` URI wich point to
        extension standart. Extension can have an `elements` of type
        `xml.etree.ElementTree.Element`. Addtional xml attributes are welcome.

            Parameters
            :param: application: URI of specification of extension
            :param extra_attrib: list additionsl xml attributes
                for xml extension
            :param content: list of `xml.etree.ElementTree.Elements`,
                content of extension

        """
        self.application = application
        self.extra_attrib = extra_attrib
        self.content = content

    def _to_element(self) -> ET.Element:
        """Extention to `xml.etree.ElementTree.Element` conversion."""
        el = ET.Element('extension',
                        attrib={'application': self.application,
                                **self.extra_attrib},)
        el.extend(self.content)
        return el

    @staticmethod
    def _from_element(element: ET.Element) -> 'Extension':
        """`xml.etree.ElementTree.Element` to Extension coversion."""
        application = _Parser.urify(element.get("application"))
        if application is None:
            raise TypeError(
                "Extension parsing missing attribute `application`")
        attribs = dict(
            [item for item in element.items() if item[0] != "application"])
        return Extension(application=application,
                         extra_attrib=attribs,
                         content=list(element))


@dataclass
class Link:
    """Object representation of `link` element.

    The link element allows XSPF to be extended without the use of
    XML namespaces.

    Content 2 arguments:
        `rel` - URI of resourse type. (required)
        `content` - URI of resourse.
    """

    rel: URI
    content: URI = ''

    @classmethod
    def _from_element(cls, element):
        rel = _Parser.urify(element.get('rel'))
        if rel is None:
            raise TypeError("`rel` attribute of link is missing\n"
                            f"{ET.tostring(element)}")
        return cls(rel=rel, content=_Parser.urify(element.text))

    def _to_element(self) -> ET.Element:
        el = ET.Element('link', {'rel': str(self.rel)})
        el.text = str(self.content)
        return el


@dataclass()
class Meta:
    """Object representation of `meta` element.

    The meta element allows metadata fields to be added to XSPF.

    Content 2 arguments:
        `rel` -- URI of resourse type. (required)
        `content` -- value of metadata element. Usualy plain text.
    """

    rel: URI
    content: str = ''

    @classmethod
    def _from_element(cls, element):
        # Check for markup.
        if len(list(element)) > 0:
            raise ValueError("Got nested elements in expected text. "
                             "Probably, this is unexpected HTML insertion.\n"
                             f"{ET.tostring(element)}")
        rel = _Parser.urify(element.get('rel'))
        if rel is None:
            raise TypeError("`rel` attribute of meta is missing\n"
                            f"{ET.tostring(element)}")
        return cls(rel=rel, content=element.text)

    def _to_element(self) -> ET.Element:
        el = ET.Element('meta', {'rel': str(self.rel)})
        el.text = str(self.content)
        return el


class Attribution:
    """Object representation of `attribution` element.

    Can contain `location` attribute or `identifier` atribute or both.
    """

    __slots__ = ['location', 'identifier']

    def __init__(self, location: Optional[URI] = None,
                 identifier: Optional[URI] = None):
        """Create new attribution.

        Generate representation of `Attribution` element of
        `xpsf_lib.Playlist`.

        Parameters.
        :param location: -- data for `location` attribution.
        :param identifier: -- data for `identifier` attribution.

        It's obvious to add something to `location` to create location
        attribution. Or, you can add only `identifier` to create identifier
        attribute. You also can add both `attribution` and `location` field to
        create 2 attribution elements. Not putting both attributes is little
        odd.
        """
        self.location = location
        self.identifier = identifier

    def __repr__(self) -> repr:
        """Representation of `Attribute` object and that fields."""
        resp = "<Attribution {"
        if self.location is not None:
            resp += f"location={self.location}"
            if self.identifier is not None:
                resp += ', '
        if self.identifier is not None:
            resp += f"identifier={self.identifier}"
        resp += "}>"
        return resp

    def xml_elements(self):
        """Create generator of xml representation."""
        if self.location is not None:
            el = ET.Element('location')
            el.text = str(urlparse.quote(self.location, safe='/:'))
            yield el
        if self.identifier is not None:
            el = ET.Element('identifier')
            el.text = str(self.identifier)
            yield el

    @classmethod
    def _from_element(cls, element) -> 'Attribution':
        if element.tag == ''.join(['{', NS['xspf'], '}location']):
            return Attribution(
                location=urlparse.unquote(_Parser.urify(element.text.strip())))
        elif element.tag == ''.join(['{', NS['xspf'], '}identifier']):
            return Attribution(identifier=_Parser.urify(element.text))
        else:
            # No `location` and `identifier` attribution is not allowed
            raise TypeError("Forbidden element in attribution.\n"
                            "Only `location` and `identifier` is "
                            "allowed.\n"
                            f"Got {ET.tostring(element)}.")


class Track():
    """Track info class."""

    def __init__(self,
                 location: Union[Iterable[URI], URI, None] = None,
                 identifier: Union[Iterable[URI], URI, None] = None,
                 title: Optional[str] = None,
                 creator: Optional[str] = None,
                 annotation: Optional[str] = None,
                 info: Optional[URI] = None,
                 image: Optional[URI] = None,
                 album: Optional[str] = None,
                 trackNum: Optional[int] = None,
                 duration: Optional[int] = None,
                 link: Iterable[Link] = [],
                 meta: Iterable[Meta] = [],
                 extension: Iterable[Extension] = []) -> None:
        """Track info class.

        Generate instances of tracks, ready to be put in Playlist class.

        Parameters
        :param location: URI or list of URI of resourse to be rendered
        :param identifier: canonical ID or list of ID for this resourse
        :param title: name o fthe track
        :param creator: name of creator of resourse
        :param annotation: comment on the track
        :param info: IRI of a place where info of this resourse can be
        founded
        :param image: URI of an image to display for the duration of the
        track
        :param album: name of the collection from which this resourse comes
        :param trackNum: integer giving the ordinal position of the media
        on the album
        :param duration: the time to render a resourse in milliseconds
        :param link: The link elements allows playlist extended without the
        use of XML namespace. List of entities of `xspf_lib.Link`.
        :param meta: Metadata fields of playlist.
        List of entities of `xspf_lib.Meta`.
        :param extension: Extension of non-XSPF XML elements. Must be a list
        tuples like `[Extension, ...]`

        """
        if isinstance(location, URI):
            self.location = [location]
        else:
            self.location = location
        if isinstance(identifier, URI):
            self.identifier = [identifier]
        else:
            self.identifier = identifier
        self.title = title
        self.creator = creator
        self.annotation = annotation
        self.info = info
        self.image = image
        self.album = album
        if trackNum is not None:
            if not int(trackNum) > 0:
                raise ValueError("""trackNum must be greater than zero""")
            self.trackNum = int(trackNum)
        else:
            self.trackNum = None
        if duration is not None:
            if int(duration) < 0:
                raise ValueError("""duration must be a non negative integer""")
            self.duration = duration
        else:
            self.duration = None
        self.link = list(link)
        self.meta = list(meta)
        self.extension = list(extension)

    __slots__ = ('location', 'identifier', 'title', 'creator', 'annotation',
                 'info', 'image', 'album', 'trackNum', 'duration', 'link',
                 'meta', 'extension')

    def __repr__(self) -> str:
        """Return representation `repr(self)`."""
        repr = "<Track"
        if self.title is not None:
            repr += f'"{self.title}"'
        else:
            repr += " NONAME"
        if self.location is not None:
            repr += f' at "{self.location[0]}">'
        else:
            repr += '>'
        return repr

    @property
    def xml_element(self) -> ET.Element:
        """Create `xml.ElementTree.Element` of the track."""
        track = ET.Element('track')
        if self.location is not None:
            for loc in self.location:
                ET.SubElement(track, 'location').text = \
                    str(urlparse.quote(loc, safe='/:'))
        if self.identifier is not None:
            for id in self.identifier:
                ET.SubElement(track, 'identifier').text = str(id)
        if self.title is not None:
            ET.SubElement(track, 'title').text = str(self.title)
        if self.creator is not None:
            ET.SubElement(track, 'creator').text = str(self.creator)
        if self.annotation is not None:
            ET.SubElement(track, 'annotation').text = str(self.annotation)
        if self.info is not None:
            ET.SubElement(track, 'info').text = str(self.info)
        if self.image is not None:
            ET.SubElement(track, 'image').text = str(self.image)
        if self.album is not None:
            ET.SubElement(track, 'album').text = str(self.album)
        if self.trackNum is not None:
            ET.SubElement(track, 'trackNum').text = str(self.trackNum)
        if self.duration is not None:
            ET.SubElement(track, 'duration').text = str(self.duration)
        track.extend(link._to_element() for link in self.link)
        track.extend(meta._to_element() for meta in self.meta)
        track.extend([extension._to_element() for extension in self.extension])
        return track

    def xml_string(self) -> str:
        """Return XML representation of track."""
        return ET.tostring(self.xml_element, encoding="UTF-8").decode()

    @staticmethod
    def _parse_xml(element):
        return _TrackParser(element).parse()


class Playlist(UserList):
    """Playlist info class."""

    def __init__(self,
                 title: Optional[str] = None,
                 creator: Optional[str] = None,
                 annotation: Optional[str] = None,
                 info: Optional[URI] = None,
                 location: Optional[URI] = None,
                 identifier: Optional[URI] = None,
                 image: Optional[URI] = None,
                 license: Optional[URI] = None,
                 attribution: Iterable[Union['Playlist', Attribution]] = [],
                 link: Iterable[Link] = [],
                 meta: Iterable[Meta] = [],
                 extension: Iterable[Extension] = [],
                 trackList: Iterable[Track] = []) -> None:
        """
        Playlist info class.

        Parameters:
        :param title: Title of the playlist.
        :param creator: Name of the entity that authored playlist.
        :param annotation: Comment of the playlist.
        :param info: URI of a web page to find out more about playlist.
        :param location: Source URI for the playlist
        :param identifier: Canonical URI for the playlist.
        :param image: URI of image to display in the absence of track image.
        :param license: URI of resource that describes the licence of playlist.
        :param attribution: List of attributed playlists or `Attribution`
        entities.
        :param link: The link elements allows playlist extended without the
        use of XML namespace. List of entities of `xspf.Link`.
        :param meta: Metadata fields of playlist.
        List of entities of `xspf.Meta`.
        :param extension: Extension of non-XSPF XML elements. Must be a list
            of xspf_lib.Extension objects.`
        :param trackList: Ordered list of track elements.

        """
        self.title = title
        self.creator = creator
        self.annotation = annotation
        self.info = info
        self.location = location
        self.identifier = identifier
        self.image = image
        self.date = datetime.now(timezone.utc).astimezone()
        self.license = license
        self.attribution = attribution
        self.link = list(link)
        self.meta = list(meta)
        self.extension = list(extension)
        self.trackList = list(trackList)

    @property
    def data(self):
        """`self.data` member required by `collections.UserList` class."""
        return self.trackList

    def __repr__(self):
        """Return representation `repr.self`."""
        repr = "<Playlist"
        if self.title is not None:
            repr += f' "{self.title}"'
        repr += f': {len(self.trackList)} tracks>'
        return repr

    @property
    def xml_element(self) -> ET.Element:
        """Return `xml.ElementTree.Element` of the playlist."""

        playlist = ET.Element('playlist', {'version': "1",
                                           'xmlns': NS['xspf']})

        # Setting bunch of parameters.
        for parameter in ['title', 'creator', 'annotation']:
            attr = self.__dict__[parameter]
            if attr is not None:
                ET.SubElement(playlist, parameter).text = str(attr)

        # Setting bunch of uri parameters.
        for uri_param in ['info', 'location', 'identifier', 'image']:
            attr = self.__dict__[uri_param]
            if attr is not None:
                ET.SubElement(playlist, uri_param).text = str(quote(attr))

        ET.SubElement(playlist, 'date').text = self.date.isoformat()
        if self.license is not None:
            ET.SubElement(playlist, 'license').text = str(quote(self.license))
        if len(self.attribution) > 0:
            attribution = ET.SubElement(playlist, 'attribution')
            for attr in self.attribution[0:9]:
                if attr.location is not None:
                    ET.SubElement(attribution, 'location').text = attr.location
                if attr.identifier is not None:
                    ET.SubElement(attribution, 'identifier').text = \
                        attr.identifier
        playlist.extend(link._to_element() for link in self.link)
        playlist.extend(meta._to_element() for meta in self.meta)
        playlist.extend(
            [extension._to_element() for extension in self.extension])
        ET.SubElement(playlist, 'trackList').extend(
            (track.xml_element for track in self.trackList))
        return playlist

    @property
    def xml_eltree(self) -> ET.ElementTree:
        """Return `xml.etree.ElementTree.ElementTree` object of playlist."""
        return ET.ElementTree(element=self.xml_element)

    def xml_string(self) -> str:
        """Return XML representation of playlist."""
        return ET.tostring(self.xml_element, encoding="UTF-8").decode()

    def write(self, file_or_filename, encoding="utf-8") -> None:
        """Write playlist into file."""
        self.xml_eltree.write(file_or_filename,
                              encoding="UTF-8",
                              method="xml",
                              short_empty_elements=True,
                              default_namespace=NS["xspf"],
                              xml_declaration=True)

    @classmethod
    def parse(cls, filename) -> 'Playlist':
        """Parse XSPF file into `xspf_lib.Playlist` entity."""
        return cls._parse_xml(ET.parse(filename).getroot())

    @classmethod
    def _parse_xml(cls, root) -> 'Playlist':
        return _PlaylistParser(root).parse()

    def _to_attribution(self) -> Attribution:
        return Attribution(location=self.location, identifier=self.identifier)


class _Parser():
    def __init__(self, xml_element):
        self.xml_element = xml_element

    # URI checker By RFC 3986
    lowalpha = 'abcdefghijklmnopqrstuvwxyz'
    upalpha = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    alpha = lowalpha + upalpha
    digit = '0123456789'
    unreserved = alpha + digit + '-._~'
    gen_delims = ':/?#[]@'
    sub_delims = '!$&\'()*+,;='
    reserved = gen_delims + sub_delims
    quoted = '%'
    uric = reserved + unreserved + quoted

    @staticmethod
    def urify(value):
        if all(char in _Parser.uric for char in value):
            return value
        else:
            raise ValueError("Only valid URI is acceptable.\n"
                             f"Got `{value}`")

    @staticmethod
    def check_element_nonleaf_content(element) -> None:
        if element.text is not None and \
                not element.text.isspace():
            raise TypeError(f"Element <{element.tag}> nonleaf "
                            "content is not allowed.\n"
                            f"| Got `{element.text}`.")

    def insert_title(self) -> None:
        title = self.get_xml_leaf_parameter_value('title')
        self.insert_parameter_if_not_null('title', title)

    def insert_creator(self) -> None:
        creator = self.get_xml_leaf_parameter_value('creator')
        self.insert_parameter_if_not_null('creator', creator)

    def insert_annotation(self) -> None:
        annotation = self.get_xml_leaf_parameter_value('annotation')
        self.insert_parameter_if_not_null('annotation', annotation)

    def insert_info(self):
        info = self.get_xml_leaf_parameter_uri_value('info')
        self.insert_parameter_if_not_null('info', info)

    def insert_image(self) -> None:
        image = self.get_xml_leaf_parameter_uri_value('image')
        self.insert_parameter_if_not_null('image', image)

    def insert_links(self) -> None:
        self.parsing_entity.link.extend(
            Link._from_element(link) for link in
            self.xml_element.findall("xspf:link", NS))

    def insert_metas(self) -> None:
        self.parsing_entity.meta.extend(
            Meta._from_element(meta) for meta in
            self.xml_element.findall("xspf:meta", NS))

    def insert_extensions(self) -> None:
        self.parsing_entity.extension.extend(
            Extension._from_element(extension) for extension in
            self.xml_element.findall('xspf:extension', NS))

    def insert_parameter_if_not_null(self, parameter_name: str,
                                     parameter_value: Union[str, int]) -> None:
        if parameter_value is not None:
            self.parsing_entity.__setattr__(parameter_name, parameter_value)

    def get_xml_leaf_parameter_value(self, parameter_name: str) -> str:
        return self._get_xml_leaf_parameter_value_with_urify(
            parameter_name,
            need_urify=False)

    def get_xml_leaf_parameter_int_value(self, parameter_name: str) -> str:
        string = self.get_xml_leaf_parameter_value(parameter_name)
        if string is not None:
            return int(string)

    def get_xml_leaf_parameter_uri_value(self, parameter_name: str) -> str:
        return self._get_xml_leaf_parameter_value_with_urify(
            parameter_name,
            need_urify=True)

    def _get_xml_leaf_parameter_value_with_urify(self,
                                                 parameter_name: str,
                                                 need_urify: bool = False) \
            -> str:
        self.check_single_element_in_root(parameter_name)
        parameter = self.xml_element.find("xspf:" + parameter_name, NS)
        if parameter is not None:
            self.__class__.check_inserted_markup(parameter)
            self.__class__.check_forbidden_element_attributes(parameter)
            ret_text = parameter.text
            if need_urify:
                ret_text = self.__class__.urify(ret_text)
            return ret_text

    def check_single_element_in_root(self, element_name: str) -> None:
        if len(self.xml_element.findall("xspf:" + element_name, NS)) > 1:
            raise TypeError(f"Got too many `{element_name}` elements in "
                            "playlist.\n"
                            f"{ET.tostring(self.xml_element)}")

    @staticmethod
    def check_inserted_markup(element) -> None:
        if len(list(element)) > 0:
            raise ValueError("Got nested elements in expected text. "
                             "Probably, this is unexpected HTML "
                             "insertion.\n"
                             f"{ET.tostring(element)}")

    @staticmethod
    def check_forbidden_element_attributes(element) -> None:
        if len(element.attrib) > 0 and \
                element.keys() != \
                ["{http://www.w3.org/XML/1998/namespace}base"]:
            raise TypeError("Element contains forbidden attribute "
                            f"{element.attrib}.\n"
                            f"{ET.tostring(element)}")


class _TrackParser(_Parser):
    def __init__(self, xml_element: ET.Element):
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
        if self.xml_element.tag != ''.join(['{', NS["xspf"], '}track']):
            raise TypeError("Track element not contain 'track' tag ",
                            "or namespace setted wrong",
                            object=self.xml_element)

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
        self.insert_trackNum()
        self.insert_duration()
        self.insert_links()
        self.insert_metas()
        self.insert_extensions()

    def insert_locations(self) -> None:
        locations = self.xml_element.findall("xspf:location", NS)
        if len(locations) > 0:
            self.parsing_entity.location = [
                urlparse.unquote(self.__class__.urify(location.text.strip()))
                for location in locations]

    def insert_identifiers(self) -> None:
        identifiers = self.xml_element.findall("xspf:identifier", NS)
        if len(identifiers) > 0:
            self.parsing_entity.identifier = [
                urlparse.unquote(self.__class__.urify(identifier.text.strip()))
                for identifier in identifiers]

    def insert_album(self) -> None:
        album = self.get_xml_leaf_parameter_value('album')
        self.insert_parameter_if_not_null('album', album)

    def insert_trackNum(self) -> None:
        trackNum = self.get_xml_leaf_parameter_int_value('trackNum')
        self.insert_parameter_if_not_null('trackNum', trackNum)

    def insert_duration(self) -> None:
        duration = self.get_xml_leaf_parameter_int_value('duration')
        self.insert_parameter_if_not_null('duration', duration)


class _PlaylistParser(_Parser):

    def __init__(self, xml_element: ET.Element):
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
        if not self.xml_element.tag[0] == '{':
            raise TypeError("Playlist namespace attribute is missing.\n"
                            f"{ET.tostring(self.xml_element)}")

    def check_for_right_namespace_string(self) -> None:
        if not self.xml_element.tag.startswith(
                ''.join(['{', NS["xspf"], '}'])):
            wrong_namespace = self.xml_element.tag.split('}')[0].lstrip('{')
            raise ValueError("Namespace is wrong string.\n"
                             f"| Expected `{NS['xspf']}`.\n"
                             f"| Got `{wrong_namespace}`.")

    def check_root_tag_name(self) -> None:
        if self.xml_element.tag != ''.join(['{', NS['xspf'], '}playlist']):
            raise ValueError("Root tag name is not correct.\n"
                             "| Expected: `playlist`.\n"
                             f"| Got: `{self.xml_element.tag.split('}')[1]}`")

    def check_version_attribute_is_exist(self) -> None:
        # Version attribute check.
        if 'version' not in self.xml_element.keys():
            raise TypeError("version attribute of playlist is missing.")

    def check_forbidden_root_attributes(self) -> None:
        root_attribs = self.xml_element.keys()
        if not (root_attribs == ['version'] or root_attribs == [
                'version', '{http://www.w3.org/XML/1998/namespace}base']):
            forbidden_attributes = list(root_attribs)
            try:
                forbidden_attributes.remove('version')
            except ValueError:
                pass
            try:
                forbidden_attributes.remove(
                    '{http://www.w3.org/XML/1998/namespace}base')
            except ValueError:
                pass
            raise TypeError("<playlist> element contains forbidden elements.\n"
                            f"{forbidden_attributes}")

    def check_value_of_version(self) -> None:
        version = int(self.xml_element.get("version"))
        # 0 version not implemented
        if version == 0:
            raise ValueError("XSPF version 0 not maintained, "
                             "switch to version 1.")
        # Another version than 1 not accepted.
        elif version != 1:
            raise ValueError(
                "The 'version' attribute must be 1.\n"
                f"Your playlist version setted to {version}.\n"
                "See http://xspf.org/xspf-v1.html#rfc.section.4.1.1.1.2")

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
        self.insert_trackList()

    def insert_location(self) -> None:
        location = self.get_xml_leaf_parameter_uri_value('location')
        self.insert_parameter_if_not_null('location', location)

    def insert_identifier(self) -> None:
        identifier = self.get_xml_leaf_parameter_uri_value('identifier')
        self.insert_parameter_if_not_null('identifier', identifier)

    def insert_license(self) -> None:
        license = self.get_xml_leaf_parameter_uri_value('license')
        self.insert_parameter_if_not_null('license', license)

    def insert_date(self) -> None:
        date_string = self.get_xml_leaf_parameter_value('date')
        if date_string is not None:
            date_string = date_string.strip()
            date_object = datetime.fromisoformat(date_string)
            self.insert_parameter_if_not_null('date', date_object)

    def insert_attributions(self) -> None:
        self.check_single_element_in_root('attribution')
        attribution = self.xml_element.find("xspf:attribution", NS)
        if attribution is not None:
            self.__class__.check_element_nonleaf_content(attribution)
            self.parsing_entity.attribution.extend(
                Attribution()._from_element(attr)
                for attr in attribution)

    def insert_trackList(self) -> None:
        self.check_trackList_is_only_one()
        trackList = self.xml_element.find("xspf:trackList", NS)
        self.__class__.check_element_nonleaf_content(trackList)
        self.parsing_entity.trackList.extend(
            Track._parse_xml(track) for track in trackList)

    def check_trackList_is_only_one(self) -> None:
        self.check_single_element_in_root('trackList')
        trackList = self.xml_element.find("xspf:trackList", NS)
        if trackList is None:
            raise TypeError("trackList element not founded.")
