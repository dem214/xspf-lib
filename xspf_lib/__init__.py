"""Module helps to work with xspf playlists.

:examples:
>>> import xspf_lib as xspf
>>> killer_queen = xspf.Track(location="file:///home/music/killer_queen.mp3", title="Killer Queen", creator="Queen", album="Sheer Heart Attack", trackNum=2, duration=177000, annotation="#2 in GB 1975", info="https://ru.wikipedia.org/wiki/Killer_Queen", image="file:///home/images/killer_queen_cover.png")
>>> anbtd = xspf.Track(location=["https://freemusic.example.com/loc.ogg", "file:///home/music/anbtd.mp3"], title="Another One Bites the Dust", creator="Queen", identifier="id1.group", link=[("link.namespace", "link.uri.info")], meta=[("meta.namespace", "METADATA_INFO")])
>>> playlist = xspf.Playlist(title="Some Tracks", creator="myself", annotation="I did this only for examples!.", trackList=[killer_queen, anbtd])
>>> print(playlist.xml_string())
<playlist version="1" xmlns="http://xspf.org/ns/0/"><title>Some Tracks</title><creator>myself</creator><annotation>I did this only for examples!.</annotation><date>2020-02-03T14:29:59.199202+03:00</date><trackList><track><location>file:///home/music/killer_queen.mp3</location><title>Killer Queen</title><creator>Queen</creator><annotation>#2 in GB 1975</annotation><info>https://ru.wikipedia.org/wiki/Killer_Queen</info><image>file:///home/images/killer_queen_cover.png</image><album>Sheer Heart Attack</album><trackNum>2</trackNum><duration>177000</duration></track><track><location>https://freemusic.example.com/loc.ogg</location><location>file:///home/music/anbtd.mp3</location><identifier>id1.group</identifier><title>Another One Bites the Dust</title><creator>Queen</creator><link rel="link.namespace">link.uri.info</link><meta rel="meta.namespace">METADATA_INFO</meta></track></trackList></playlist>

"""
import xml.etree.ElementTree as ET
from typing import Iterable, Optional, Union, Tuple
from datetime import datetime, timezone
from collections import UserList

URI = str
NS = {'xspf': "http://xspf.org/ns/0/"}


class Track():
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
                 link: Iterable[Tuple[URI, URI]] = list(),
                 meta: Iterable[Tuple[URI, str]] = list(),
                 extension: Iterable[Tuple[URI, ET.Element]] = list()) -> None:
        """Track info class.

        Generate instances of tracks, ready to be put in Playlist class
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
            use of XML namespace. Must be a list of tuples like
            `[(URI_of_resource_type, URI_of_resource), ...]`.
        :param meta: Metadata fields of playlist. Must be a list of tuples
            like `[(URI_of_resource_defining_the_metadata, value), ...]`
        :param extension: Extension of non-XSPF XML elements. Must be a list
            tuples like `[(URI_of_application, xml.etree.ElementTree.Element),
            ...]`
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
        self.link = link
        self.meta = meta
        self.extension = extension

    __slots__ = ('location', 'identifier', 'title', 'creator', 'annotation',
                 'info', 'image', 'album', 'trackNum', 'duration', 'link',
                 'meta', 'extension')

    def __repr__(self):
        """Return representation `repr(self)`."""
        repr = "<Track"
        if self.Title is not None:
            repr += f'"{self.name}"'
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
                ET.SubElement(track, 'location').text = str(loc)
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
        for link in self.link:
            ET.SubElement(track, 'link', {'rel': str(link[0])})\
                .text = str(link[1])
        for meta in self.meta:
            ET.SubElement(track, 'meta', {'rel': str(meta[0])})\
                .text = str(meta[1])
        for extension in self.extension:
            ext = ET.SubElement(track, 'extension',
                                {'application': str(extension[0])})
            ext.append(extension[1])
        return track

    def xml_string(self, *args, **kwargs):
        """Return XML representation of track."""
        return ET.tostring(self.xml_element, encoding="UTF-8").decode()

    def _parse_xml(element):
        if element.tag != ''.join(['{', NS["xspf"], '}track']):
            raise TypeError("Track element not contain 'track' tag ",
                            "or namespace setted wrong", object=element)
        track = Track()
        locations = element.findall("xspf:location", NS)
        if len(locations) > 0:
            track.location = [location.text for location in locations]
        identifiers = element.findall("xspf:identifiers", NS)
        if len(identifiers) > 0:
            track.identifier = [identifier.text for identifier in identifiers]
        def get_simple_element_and_set_attr(element, track, attr):
            param = element.find("xspf:" + attr, NS)
            if param is not None:
                setattr(track, attr, param.text)
        get_simple_element_and_set_attr(element, track, 'title')
        get_simple_element_and_set_attr(element, track, 'creator')
        get_simple_element_and_set_attr(element, track, 'annotation')
        get_simple_element_and_set_attr(element, track, 'info')
        get_simple_element_and_set_attr(element, track, 'image')
        get_simple_element_and_set_attr(element, track, 'album')
        trackNum = element.find("xspf:trackNum", NS)
        if trackNum is not None:
            track.trackNum = int(trackNum.text)
        duration = element.find("xspf:duration", NS)
        if duration is not None:
            track.duration = int(duration.text)
        for link in element.findall("xspf:link", NS):
            track.link.append((link.get("rel"), link.text))
        for meta in element.findall("xspf:meta", NS):
            track.meta.append((link.get("rel"), meta.text))
        for extension in element.findall("xspf:extension", NS):
            track.extension.append((extension.get("application"),
                                    extension.find('.')))
        return track

class Playlist(UserList):
    def __init__(self,
                 title: Optional[str] = None,
                 creator: Optional[str] = None,
                 annotation: Optional[str] = None,
                 info: Optional[URI] = None,
                 location: Optional[URI] = None,
                 identifier: Optional[URI] = None,
                 image: Optional[URI] = None,
                 license: Optional[URI] = None,
                 attribution: Iterable['Playlist'] = list(),
                 link: Iterable[Tuple[URI, URI]] = list(),
                 meta: Iterable[Tuple[URI, str]] = list(),
                 extension: Iterable[Tuple[URI, ET.Element]] = list(),
                 trackList: Iterable[Track] = list()) -> None:
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
        :param attribution: List of attributed playlists.
        :param link: The link elements allows playlist extended without the
            use of XML namespace. Must be a list of tuples like
            `[(URI_of_resource_type, URI_of_resource), ...]`.
        :param meta: Metadata fields of playlist. Must be a list of tuples
            like `[(URI_of_resource_defining_the_metadata, value), ...]`
        :param extension: Extension of non-XSPF XML elements. Must be a list
            tuples like `[(URI_of_application, xml.etree.ElementTree.Element),
            ...]`
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
        self.link = link
        self.meta = meta
        self.extension = extension
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
        if self.title is not None:
            ET.SubElement(playlist, 'title').text = str(self.title)
        if self.creator is not None:
            ET.SubElement(playlist, 'creator').text = str(self.creator)
        if self.annotation is not None:
            ET.SubElement(playlist, 'annotation').text = str(self.annotation)
        if self.info is not None:
            ET.SubElement(playlist, 'info').text = str(self.info)
        if self.location is not None:
            ET.SubElement(playlist, 'location').text = str(self.location)
        if self.identifier is not None:
            ET.SubElement(playlist, 'identifier').text = str(self.identifier)
        if self.image is not None:
            ET.SubElement(playlist, 'image').text = str(self.image)
        ET.SubElement(playlist, 'date').text = self.date.isoformat()
        if self.license is not None:
            ET.SubElement(playlist, 'license').text = str(self.license)
        if len(self.attribution) > 0:
            attribution = ET.SubElement(playlist, 'attribution')
            for attr in self.attribution[0:9]:
                ET.SubElement(attribution, 'location').text = attr.location
                ET.SubElement(attribution, 'identifier').text = attr.identifier
        for link in self.link:
            ET.SubElement(playlist, 'link', {'rel': str(link[0])})\
                .text = str(link[1])
        for meta in self.meta:
            ET.SubElement(playlist, 'meta', {'rel': str(meta[0])})\
                .text = str(meta[1])
        for extension in self.extension:
            ext = ET.SubElement(playlist, 'extension',
                                {'application': str(extension[0])})
            ext.append(extension[1])
        ET.SubElement(playlist, 'trackList').extend(
            (track.xml_element for track in self.trackList))
        return playlist

    def dump(self) -> None:
        """Return XML formated entity of track."""
        return ET.dump(self.xml_element)

    @property
    def xml_eltree(self) -> ET.ElementTree:
        """Return `xml.etree.ElementTree.ElementTree` object of playlist."""
        return ET.ElementTree(element=self.xml_element)

    def xml_string(self):
        """Return XML representation of playlist."""
        return ET.tostring(self.xml_element, encoding="UTF-8").decode()

    def write(self, file):
        """Write playlist into file."""
        self.xml_eltree.write(file, encoding="UTF-8", xml_declaration=True)

    @classmethod
    def parse(cls, filename):
        tree = ET.parse(filename)
        root = tree.getroot()
        return cls._parse_xml(root)

    @staticmethod
    def _parse_xml(root):
        playlist = Playlist()
        def get_simple_element_and_set_attr(root, playlist, attr):
            param = root.find("xspf:" + attr, NS)
            if param is not None:
                playlist.__setattr__(attr, param.text)
        get_simple_element_and_set_attr(root, playlist, 'title')
        get_simple_element_and_set_attr(root, playlist, 'creator')
        get_simple_element_and_set_attr(root, playlist, 'annotation')
        get_simple_element_and_set_attr(root, playlist, 'info')
        get_simple_element_and_set_attr(root, playlist, 'location')
        get_simple_element_and_set_attr(root, playlist, 'identifier')
        get_simple_element_and_set_attr(root, playlist, 'image')
        get_simple_element_and_set_attr(root, playlist, 'license')
        date = root.find("xspf:date", NS)
        if date is not None:
            playlist.date = datetime.fromisoformat(date.text)
        attribution = root.find("xspf:date", NS)
        if attribution is not None:
            # TODO: invent way to parse attribution
            pass
        for link in root.findall("xspf:link", NS):
            playlist.link.append((link.get("rel"), link.text))
        for meta in root.findall("xspf:meta", NS):
            playlist.meta.append((link.get("rel"), meta.text))
        for extension in root.findall("xspf:extension", NS):
            playlist.extension.append((extension.get("application"),
                                       extension.find('.')))
        for track in root.find("xspf:trackList", NS):
            playlist.append(Track._parse_xml(track))

        return playlist

    class BadVersionError(Exeption)
