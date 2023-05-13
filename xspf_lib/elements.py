from collections import UserList
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Iterable, Iterator, List, Optional, Union
from urllib import parse as urlparse
from xml.etree import ElementTree as Et

from .base import XMLAble
from .builders import build_playlist, build_track
from .constants import XML_NAMESPACE
from .types import URI
from .utils import quote, urify


@dataclass()
class Extension(XMLAble):
    """
    Class for XML extensions of XSPF playlists and tracks.

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

    application: URI
    extra_attrib: Dict[str, str] = field(default_factory=dict)
    content: List[Et.Element] = field(default_factory=list)

    def to_xml_element(self) -> Et.Element:
        """Extension to `xml.etree.ElementTree.Element` conversion."""
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
        `rel` - URI of resource type.
        `content` - URI of resource.
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
        `rel` -- URI of resource type.
        `content` -- value of metadata element. Usually plain text.
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


@dataclass()
class Attribution(XMLAble):
    """Object representation of `attribution` element.

    Can contain `location` attribute or `identifier` atribute or both.

    Parameters.
        :param location: -- data for `location` attribution.
        :param identifier: -- data for `identifier` attribution.

        It's obvious to add something to `location` to create location
        attribution. Or, you can add only `identifier` to create identifier
        attribute. You also can add both `attribution` and `location` field to
        create 2 attribution elements. Not putting both attributes is little
        odd.
    """

    location: Optional[URI] = None
    identifier: Optional[URI] = None

    def xml_elements(self) -> Iterator[Et.Element]:
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
        element = Et.Element("attribution")
        element.extend(self.xml_elements())
        return element

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
                f"Got {str(Et.tostring(element))}."
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
        link: Union[Iterable[Link], None] = None,
        meta: Union[Iterable[Meta], None] = None,
        extension: Union[Iterable[Extension], None] = None,
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
        if isinstance(location, URI):
            location = [location]
        elif location is None:
            location = []
        self.location = list(location)
        if isinstance(identifier, URI):
            identifier = [identifier]
        elif identifier is None:
            identifier = []
        self.identifier = list(identifier)
        self.title = title
        self.creator = creator
        self.annotation = annotation
        self.info = info
        self.image = image
        self.album = album
        self.trackNum = trackNum
        self.duration = duration
        self.link: List[Link] = list(link) if link is not None else []
        self.meta: List[Meta] = list(meta) if meta is not None else []
        self.extension: List[Extension] = (
            list(extension) if extension is not None else []
        )

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
    def trackNum(self) -> Optional[int]:
        return self.__trackNum

    @trackNum.setter
    def trackNum(self, value: Optional[int]) -> None:
        if (
            value is not None and value < 0
        ):  # modified by @gdalik in order to include trackNum == 0
            raise ValueError(
                "trackNum must be non negative number.\n"
                "| Expected: {0, 1, 2, ..}\n"
                f"| Got: {value}"
            )
        self.__trackNum = value

    @property
    def duration(self) -> Optional[int]:
        return self.__duration

    @duration.setter
    def duration(self, value: Optional[int]) -> None:
        if value is not None and value < 0:
            raise ValueError(
                "duration must be a non negative integer\n"
                "| Expected: {0, 1, 2, ..}\n"
                f"| Got: {value}"
            )
        self.__duration = value

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


@dataclass(repr=False)
class Playlist(UserList, XMLAble):
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

    title: Optional[str] = None
    creator: Optional[str] = None
    annotation: Optional[str] = None
    info: Optional[URI] = None
    location: Optional[URI] = None
    identifier: Optional[URI] = None
    image: Optional[URI] = None
    date: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc).astimezone()
    )
    license: Optional[URI] = None
    attribution: List[Union["Playlist", Attribution]] = field(default_factory=list)
    link: List[Link] = field(default_factory=list)
    meta: List[Meta] = field(default_factory=list)
    extension: List[Extension] = field(default_factory=list)
    trackList: List[Track] = field(default_factory=list)

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
