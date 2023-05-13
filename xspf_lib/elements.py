from collections import UserList
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Dict, Iterable, Optional, Union
from urllib import parse as urlparse
from xml.etree import ElementTree as Et

from .base import XMLAble
from .builders import _Builder, build_playlist, build_track
from .constants import XML_NAMESPACE
from .types import URI
from .utils import quote, urify


class Extension(XMLAble):
    """Class for XML extensions of XSPF playlists and tracks."""

    __slots__ = ["application", "extra_attrib", "content"]

    def __init__(
        self,
        application: URI,
        extra_attrib: Dict[str, str] = {},
        content: Iterable[Et.Element] = [],
    ) -> None:
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

    def to_xml_element(self) -> Et.Element:
        """Extention to `xml.etree.ElementTree.Element` conversion."""
        el = Et.Element(
            "extension",
            attrib={"application": self.application, **self.extra_attrib},
        )
        el.extend(self.content)
        return el

    @staticmethod
    def parse_from_xml_element(element: Et.Element) -> "Extension":
        """`xml.etree.ElementTree.Element` to Extension coversion."""
        application = urify(element.get("application"))
        if application is None:
            raise TypeError("Extension parsing missing attribute `application`")
        attribs = dict([item for item in element.items() if item[0] != "application"])
        return Extension(
            application=application, extra_attrib=attribs, content=list(element)
        )


@dataclass
class Link(XMLAble):
    """Object representation of `link` element.

    The link element allows XSPF to be extended without the use of
    XML namespaces.

    Content 2 arguments:
        `rel` - URI of resourse type. (required)
        `content` - URI of resourse.
    """

    rel: URI
    content: URI = ""

    @staticmethod
    def parse_from_xml_element(element):
        rel = urify(element.get("rel"))
        if rel is None:
            raise TypeError(
                "`rel` attribute of link is missing\n" f"{Et.tostring(element)}"
            )
        return Link(rel=rel, content=urify(element.text))

    def to_xml_element(self) -> Et.Element:
        el = Et.Element("link", {"rel": str(self.rel)})
        el.text = str(self.content)
        return el


@dataclass()
class Meta(XMLAble):
    """Object representation of `meta` element.

    The meta element allows metadata fields to be added to XSPF.

    Content 2 arguments:
        `rel` -- URI of resourse type. (required)
        `content` -- value of metadata element. Usualy plain text.
    """

    rel: URI
    content: str = ""

    @staticmethod
    def parse_from_xml_element(element):
        # Check for markup.
        if len(list(element)) > 0:
            raise ValueError(
                "Got nested elements in expected text. "
                "Probably, this is unexpected HTML insertion.\n"
                f"{Et.tostring(element)}"
            )
        rel = urify(element.get("rel"))
        if rel is None:
            raise TypeError(
                "`rel` attribute of meta is missing\n" f"{Et.tostring(element)}"
            )
        return Meta(rel=rel, content=element.text)

    def to_xml_element(self) -> Et.Element:
        el = Et.Element("meta", {"rel": str(self.rel)})
        el.text = str(self.content)
        return el


class Attribution(XMLAble):
    """Object representation of `attribution` element.

    Can contain `location` attribute or `identifier` atribute or both.
    """

    __slots__ = ["location", "identifier"]

    def __init__(
        self, location: Optional[URI] = None, identifier: Optional[URI] = None
    ):
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
                resp += ", "
        if self.identifier is not None:
            resp += f"identifier={self.identifier}"
        resp += "}>"
        return resp

    def xml_elements(self):
        """Create generator of xml representation."""
        if self.location is not None:
            el = Et.Element("location")
            el.text = str(quote(self.location))
            yield el
        if self.identifier is not None:
            el = Et.Element("identifier")
            el.text = str(self.identifier)
            yield el

    def to_xml_element(self) -> Et.Element:
        return Et.Element("attribution").extend(self.xml_elements)

    @staticmethod
    def parse_from_xml_element(element) -> "Attribution":
        if element.tag == "".join(["{", XML_NAMESPACE["xspf"], "}location"]):
            return Attribution(location=urlparse.unquote(urify(element.text.strip())))
        elif element.tag == "".join(["{", XML_NAMESPACE["xspf"], "}identifier"]):
            return Attribution(identifier=urify(element.text))
        else:
            # No `location` and `identifier` attribution is not allowed
            raise TypeError(
                "Forbidden element in attribution.\n"
                "Only `location` and `identifier` is "
                "allowed.\n"
                f"Got {Et.tostring(element)}."
            )


class Track(XMLAble):
    """Track info class."""

    def __init__(
        self,
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
        extension: Iterable[Extension] = [],
    ) -> None:
        """Track info class.

        Generate instances of tracks, ready to be put in Playlist class.

        Parameters
        :param location: URI or list of URI of resource to be rendered
        :param identifier: canonical ID or list of ID for this resource
        :param title: name of the track
        :param creator: name of creator of resource
        :param annotation: comment on the track
        :param info: IRI of a place where info of this resource can be
        founded
        :param image: URI of an image to display for the duration of the
        track
        :param album: name of the collection from which this resource comes
        :param trackNum: integer giving the ordinal position of the media
        on the album
        :param duration: the time to render a resource in milliseconds
        :param link: The link elements allows playlist extended without the
        use of XML namespace. List of entities of `xspf_lib.Link`.
        :param meta: Metadata fields of playlist.
        List of entities of `xspf_lib.Meta`.
        :param extension: Extension of non-XSPF XML elements. Must be a list
        tuples like `[Extension, ...]`

        """
        _Builder().build_track(self, locals())

    __slots__ = (
        "location",
        "identifier",
        "title",
        "creator",
        "annotation",
        "info",
        "image",
        "album",
        "link",
        "meta",
        "extension",
    )

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
            repr += ">"
        return repr

    @property
    def trackNum(self) -> int:
        return self.__trackNum

    @trackNum.setter
    def trackNum(self, value: int) -> None:
        if value is not None:
            if value < 0:  # modified by @gdalik in order to include trackNum == 0
                raise ValueError(
                    "trackNum must be positive number.\n"
                    "| Expected: {1, 2, ..}\n"
                    f"| Got: {value}"
                )
            self.__trackNum = value
        else:
            self.__trackNum = None

    @property
    def duration(self) -> int:
        return self.__duration

    @duration.setter
    def duration(self, value: int) -> None:
        if value is not None:
            if value < 0:
                raise ValueError(
                    "duration must be a non negative integer\n"
                    "| Expected: {0, 1, 2, ..}\n"
                    f"| Got: {value}"
                )
            self.__duration = value
        else:
            self.__duration = None

    def to_xml_element(self) -> Et.Element:
        """Create `xml.ElementTree.Element` of the track."""
        return build_track(self)

    def xml_string(self) -> str:
        """Return XML representation of track."""
        return Et.tostring(self.to_xml_element(), encoding="UTF-8").decode()

    @staticmethod
    def parse_from_xml_element(element) -> "Track":
        from .parsers import TrackBaseParser

        return TrackBaseParser(element).parse()


class Playlist(UserList, XMLAble):
    """Playlist info class."""

    def __init__(
        self,
        title: Optional[str] = None,
        creator: Optional[str] = None,
        annotation: Optional[str] = None,
        info: Optional[URI] = None,
        location: Optional[URI] = None,
        identifier: Optional[URI] = None,
        image: Optional[URI] = None,
        license: Optional[URI] = None,
        attribution: Iterable[Union["Playlist", Attribution]] = [],
        link: Iterable[Link] = [],
        meta: Iterable[Meta] = [],
        extension: Iterable[Extension] = [],
        trackList: Iterable[Track] = [],
    ) -> None:
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
        self.attribution = list(attribution)
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
        repr += f": {len(self.trackList)} tracks>"
        return repr

    def to_xml_element(self) -> Et.Element:
        """Return `xml.ElementTree.Element` of the playlist."""
        return build_playlist(self)

    @property
    def xml_eltree(self) -> Et.ElementTree:
        """Return `xml.etree.ElementTree.ElementTree` object of playlist."""
        return Et.ElementTree(element=self.to_xml_element())

    def xml_string(self) -> str:
        """Return XML representation of playlist."""
        return Et.tostring(self.to_xml_element(), encoding="UTF-8").decode()

    def write(self, file_or_filename, encoding="utf-8") -> None:
        """Write playlist into file."""
        self.xml_eltree.write(
            file_or_filename,
            encoding="UTF-8",
            method="xml",
            short_empty_elements=True,
            xml_declaration=True,
        )

    @classmethod
    def parse(cls, filename) -> "Playlist":
        """Parse XSPF file into `xspf_lib.Playlist` entity."""
        return cls.parse_from_xml_element(Et.parse(filename).getroot())

    @staticmethod
    def parse_from_xml_element(root) -> "Playlist":
        from .parsers import PlaylistBaseParser

        return PlaylistBaseParser(root).parse()

    def _to_attribution(self) -> Attribution:
        return Attribution(location=self.location, identifier=self.identifier)
