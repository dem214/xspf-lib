from typing import List

class Track():
    def __init__(location: List[str] = None,
                 identifier: List[str] = None,
                 title: str = None,
                 creator: str = None,
                 annotation: str = None,
                 info: str = None,
                 image: str = None,
                 album: str = None,
                 trackNum: int = None,
                 duration: int = None,
                 link = None,
                 meta = None,
                 extension = None):
        '''Track info class

        Generate instances of tracks, ready to be put in Playlist class
        :param location: URI of resourse to be rendered
        :param identifier: canonical ID for this resourse
        :param title: name o fthe track
        :param creator: name of creator of resourse
        :param annotation: comment on the track
        :param info: IRI of a place where info of this resourse can be founded
        :param image: URI of an image to display for the duration of the track
        :param album: name of the collection from which this resourse comes
        :param trackNum: integer giving the ordinal position of the media on the album
        :param duration: the time to render a resourse in milliseconds
        :param link:
        :param meta:
        :param extensions:
        '''
        self.location = location
        self.identifier = identifier
        self.title = title
        self.creator = creator
        self.annotation = annotation
        self.info = info
        self.image = image
        self.album = album
        self.trackNum = trackNum
        self.duration = duration
        self.link = link
        self.meta = meta
        self.extension = extension
        return self

    __slots__ = ('location', 'identifier', 'title', 'creator', 'annotation',
                 'info', 'image', 'album', 'trackNum', 'duration', 'link',
                 'meta', 'extension')
