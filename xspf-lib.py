import xml.etree.ElementTree as ET
from typing import Iterable, Optional, Union
from datetime import datetime, timezone

URI = str


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
                 link=None,
                 meta=None,
                 extension=None) -> None:
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
        :param link:
        :param meta:
        :param extensions:
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

    @property
    def xml_element(self) -> ET.Element:
        """Create xml.ElementTree.Element of the track."""
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
        # TODO: add link to elements
        # TODO: add meta to elements
        # TODO: add extension to elements
        return track

    def dump(self):
        """Return XML formated entity of track."""
        return ET.dump(self.xml_element)

class Playlist():
    def __init__(self,
                 title: Optional[str] = None,
                 creator: Optional[str] = None,
                 annotation: Optional[str] = None,
                 info: Optional[URI] = None,
                 location: Optional[URI] = None,
                 identifier: Optional[URI] = None,
                 image: Optional[URI] = None,
                 license: Optional[URI] = None,
                 attribution=None,
                 link=None,
                 meta=None,
                 extension=None,
                 trackList: Optional[Iterable[Track]] = list()) -> None:
        """
        Parameters:
        :param title: Title of the playlist.
        :param creator: Name of the entity that authored playlist.
        :param annotation: Comment of the playlist.
        :param info: URI of a web page to find out more about playlist.
        :param location: Source URI for the playlist
        :param identifier: Canonical URI for the playlist.
        :param image: URI of image to display in the absence of track image.
        :param license: URI of resource that describes the licence of playlist.
        :param attribution:
        :param link:
        :param meta:
        :param extension:
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
    def xml_element(self) -> ET.Element:
        """Create xml.ElementTree.Element of the playlist."""
        playlist = ET.Element('playlist', {'version': "1",
                                           'xmlns': "http://xspf.org/ns/0/"})
        if self.title is not None:
            ET.SubElement(playlist, 'title').text = str(self.title)
        if self.creator is not None:
            ET.SubElement(playlist, 'creator').text = str(self.creator)
        if self.annotation is not None:
            ET.SubElement(playlist, 'annotation').text = str(self.annotation)
        if self.info is not None:
            ET.SubElement(playlist, 'title').text = str(self.info)
        if self.location is not None:
            ET.SubElement(playlist, 'location').text = str(self.location)
        if self.identifier is not None:
            ET.SubElement(playlist, 'identifier').text = str(self.identifier)
        if self.image is not None:
            ET.SubElement(playlist, 'image').text = str(self.image)
        ET.SubElement(playlist, 'date').text = self.date.isoformat()
        if self.license is not None:
            ET.SubElement(playlist, 'license').text = str(self.license)
        # TODO: attribution
        # TODO: link
        # TODO: meta
        # TODO: extension
        ET.SubElement(playlist, 'trackList').extend(
            (track.xml_element for track in self.trackList))
        return playlist

    def dump(self) -> None:
        """Return XML formated entity of track."""
        return ET.dump(self.xml_element)

    @property
    def xml_eltree(self) -> ET.ElementTree:
        """Return xml.etree.ElementTree.ElementTree object of playlist."""
        return ET.ElementTree(element=self.xml_element)

    def write(self, file):
        self.xml_eltree.write(file, encoding="UTF-8", xml_declaration=True)

tr = Track(title='pl1')
tr2 = Track(location='here')
tr3 = Track(location=['here', 'we', 'go'])
pl = Playlist(title='pl', trackList=[tr, tr2, tr3])
pl.write('pl.xspf')
