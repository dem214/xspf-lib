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


class _Uric_helper:
    __slots__ = {}
    # By RFC 3986
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
        if all(char in _Uric_helper.uric for char in value):
            return value
        else:
            raise ValueError("Only valid URI is acceptable.\n"
                             f"Got `{value}`")


urify = _Uric_helper.urify


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
        application = urify(element.get("application"))
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
        rel = urify(element.get('rel'))
        if rel is None:
            raise TypeError("`rel` attribute of link is missing\n"
                            f"{ET.tostring(element)}")
        return cls(rel=rel, content=urify(element.text))

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
        rel = urify(element.get('rel'))
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
                location=urlparse.unquote(urify(element.text.strip())))
        elif element.tag == ''.join(['{', NS['xspf'], '}identifier']):
            return Attribution(identifier=urify(element.text))
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
        if element.tag != ''.join(['{', NS["xspf"], '}track']):
            raise TypeError("Track element not contain 'track' tag ",
                            "or namespace setted wrong", object=element)
        # Track nonleaf content checking.
        if element.text is not None and not element.text.isspace():
            raise TypeError("Track nonleaf content is not allowed.\n"
                            f"| Got `{element.text}`.")
        track = Track()
        locations = element.findall("xspf:location", NS)
        if len(locations) > 0:
            track.location = [urlparse.unquote(urify(location.text.strip()))
                              for location in locations]
        identifiers = element.findall("xspf:identifier", NS)
        if len(identifiers) > 0:
            track.identifier = [
                urlparse.unquote(urify(identifier.text.strip()))
                for identifier in identifiers]

        def get_simple_element_and_set_attr(element, track, attr):
            params = element.findall("xspf:" + attr, NS)
            if len(params) == 1:
                param = params[0]
                # Check for inserted markup.
                if len(list(param)) > 0:
                    raise ValueError("Got nested elements in expected text. "
                                     "Probably, this is unexpected HTML "
                                     "insertion.\n"
                                     f"{ET.tostring(param)}")
                # Chech for forbidden attributes
                if len(param.attrib) > 0 and \
                        param.keys() != \
                        ["{http://www.w3.org/XML/1998/namespace}base"]:
                    raise TypeError("Element contains forbidden attribute "
                                    f"{param.attrib}.\n"
                                    f"{ET.tostring(param)}")
                track.__setattr__(attr, param.text)
            # non-multiple elements of param check
            elif len(params) > 1:
                raise TypeError(f"Got too many `{attr}` elements in track."
                                f"{ET.tostring(element)}")

        def get_simple_uri_element_and_set_attr(element, track, attr):
            params = element.findall("xspf:" + attr, NS)
            if len(params) == 1:
                param = params[0]
                # Chech for forbidden attributes
                if len(param.attrib) > 0 and \
                        param.keys() != \
                        ["{http://www.w3.org/XML/1998/namespace}base"]:
                    raise TypeError("Element contains forbidden attribute "
                                    f"{param.attrib}.\n"
                                    f"{ET.tostring(param)}")
                track.__setattr__(attr, urify(param.text))
            # non-multiple elements of param check
            elif len(params) > 1:
                raise TypeError(f"Got too many `{attr}` elements in track."
                                f"{ET.tostring(element)}")

        get_simple_element_and_set_attr(element, track, 'title')
        get_simple_element_and_set_attr(element, track, 'creator')
        get_simple_element_and_set_attr(element, track, 'annotation')
        get_simple_uri_element_and_set_attr(element, track, 'info')
        get_simple_uri_element_and_set_attr(element, track, 'image')
        get_simple_element_and_set_attr(element, track, 'album')
        trackNums = element.findall("xspf:trackNum", NS)
        if len(trackNums) == 1:
            track.trackNum = int(trackNums[0].text)
        elif len(trackNums) > 1:
            raise TypeError(f"Got too many `trackNum` elements in track."
                            f"{ET.tostring(element)}")
        durations = element.findall("xspf:duration", NS)
        if len(durations) == 1:
            track.duration = int(durations[0].text)
        elif len(durations) > 1:
            raise TypeError(f"Got too many `duration` elements in track."
                            f"{ET.tostring(element)}")
        track.link.extend(Link._from_element(link) for link in
                          element.findall("xspf:link", NS))
        track.meta.extend(Meta._from_element(meta) for meta in
                          element.findall("xspf:meta", NS))
        track.extension.extend(
            Extension._from_element(extension) for extension in
            element.findall('xspf:extension', NS))
        return track


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

        cls.__playlist_validation_xml_root_check(root)

        playlist = cls()

        def get_simple_element_and_set_attr(root, playlist, attr):
            params = root.findall("xspf:" + attr, NS)
            if len(params) == 1:
                param = params[0]
                # Check for inserted markup.
                if len(list(param)) > 0:
                    raise ValueError("Got nested elements in expected text. "
                                     "Probably, this is unexpected HTML "
                                     "insertion.\n"
                                     f"{ET.tostring(param)}")
                # Chech for forbidden attributes
                if len(param.attrib) > 0 and \
                        param.keys() != \
                        ["{http://www.w3.org/XML/1998/namespace}base"]:
                    raise TypeError("Element contains forbidden attribute "
                                    f"{param.attrib}.\n"
                                    f"{ET.tostring(param)}")
                playlist.__setattr__(attr, params[0].text)
            # non-multiple elements of param check
            elif len(params) > 1:
                raise TypeError(f"Got too many `{attr}` elements in playlist."
                                f"{ET.tostring(root)}")

        def get_simple_uri_element_and_set_attr(root, playlist, attr):
            # non-multiple elements of param check
            params = root.findall("xspf:" + attr, NS)
            if len(params) == 1:
                # Chech for forbidden attributes
                param = params[0]
                if len(param.attrib) > 0 and \
                        param.keys() != \
                        ["{http://www.w3.org/XML/1998/namespace}base"]:
                    raise TypeError("Element contains forbidden attribute "
                                    f"{param.attrib}.\n"
                                    f"{ET.tostring(param)}")
                playlist.__setattr__(attr, urify(param.text))
            elif len(params) > 1:
                raise TypeError(f"Got too many `{attr}` elements in playlist."
                                f"{ET.tostring(root)}")

        # Parsing bunch of simple elements
        for parameter in ['title', 'creator', 'annotation']:
            get_simple_element_and_set_attr(root, playlist, parameter)

        # Parsing bunch of simple uri elements
        for uri_parameter in ['info', 'location', 'identifier', 'image',
                              'license']:
            get_simple_uri_element_and_set_attr(root, playlist, uri_parameter)

        # non-multiple elements of date check
        dates = root.findall("xspf:date", NS)
        if len(dates) > 1:
            raise TypeError(f"Got too many `date` elements in playlist."
                            f"{ET.tostring(root)}")
        if len(dates) == 1:
            playlist.date = datetime.fromisoformat(dates[0].text.strip())
        # non-multiple elements of attribution check
        attributions = root.findall("xspf:attribution", NS)
        if len(attributions) > 1:
            raise TypeError(f"Got too many `attribution` elements in playlist."
                            f"{ET.tostring(root)}")
        if len(attributions) == 1:
            attribution = attributions[0]
            # Attribution nonleaf content checking.
            if attribution.text is not None and not attribution.text.isspace():
                raise TypeError("Attribution nonleaf content not allowed.\n"
                                f"Got {attribution.text}")
            playlist.attribution.extend(Attribution()._from_element(attr)
                                        for attr in attribution)
        playlist.link.extend(Link._from_element(link) for link in
                             root.findall("xspf:link", NS))
        playlist.meta.extend(Meta._from_element(meta) for meta in
                             root.findall("xspf:meta", NS))
        playlist.extension.extend(
            Extension._from_element(extension) for extension in
            root.findall('xspf:extension', NS))
        # non-multiple elements of trackList check
        trackLists = root.findall("xspf:trackList", NS)
        if len(trackLists) == 1:
            trackList = trackLists[0]
            # Non leaf content check.
            if trackList.text is not None and not trackList.text.isspace():
                raise TypeError("trackList nonleaf content not allowed.\n"
                                f"| Got: `{trackList.text}`.")
            playlist.trackList.extend(Track._parse_xml(track)
                                      for track in trackList)
        elif len(trackLists) > 1:
            raise TypeError(f"Got too many `trackList` elements in playlist."
                            f"{ET.tostring(root)}")
        elif len(trackLists) == 0:
            raise TypeError("trackList element not founded.")

        return playlist

    def _to_attribution(self) -> Attribution:
        return Attribution(location=self.location, identifier=self.identifier)

    @staticmethod
    def __playlist_validation_xml_root_check(root) -> None:
        # Check for namespace existing.
        if not root.tag[0] == '{':
            raise TypeError("Playlist namespace attribute is missing.\n"
                            f"{ET.tostring(root)}")
        # Check for right namespace string.
        if not root.tag.startswith(''.join(['{', NS["xspf"], '}'])):
            raise ValueError("Namespace is wrong string.\n"
                             f"| Expected `{NS['xspf']}`.\n"
                             f"| Got `{root.tag.split('}')[0].lstrip('{')}`.")
        # Root name check.
        if root.tag != ''.join(['{', NS['xspf'], '}playlist']):
            raise ValueError("Root tag name is not correct.\n"
                             "| Expected: `playlist`.\n"
                             f"| Got: `{root.tag.split('}')[1]}`")
        root_attribs = root.keys()
        # Version attribute check.
        if 'version' not in root_attribs:
            raise TypeError("version attribute of playlist is missing.")
        # Forbidden attribute check -- all except `version` and `base`.
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
        # Value of version checking.
        version = int(root.get("version"))
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
        # Playlist nonleaf content checking.
        if root.text is not None and not root.text.isspace():
            raise TypeError("Playlist nonleaf content is not allowed.\n"
                            f"| Got `{root.text}`.")
