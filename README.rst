========
xspf-lib
========

Library to work with xspf.

Installing
----------

Install and update via `pip`_:

.. code-block:: text

    pip install -U xspf-lib

Example
-------
1. Generating new playlist.

>>> import xspf_lib as xspf
>>> killer_queen = xspf.Track(location="file:///home/music/killer_queen.mp3",
                              title="Killer Queen",
                              creator="Queen",
                              album="Sheer Heart Attack",
                              trackNum=2,
                              duration=177000,
                              annotation="#2 in GB 1975",
                              info="https://ru.wikipedia.org/wiki/Killer_Queen",
                              image="file:///home/images/killer_queen_cover.png")
>>> anbtd = xspf.Track(location=["https://freemusic.example.com/loc.ogg",
                                 "file:///home/music/anbtd.mp3"],
                       title="Another One Bites the Dust",
                       creator="Queen",
                       identifier="id1.group",
                       link=[xspf.Link("link.namespace", "link.uri.info")],
                       meta=[xspf.Meta("meta.namespace", "METADATA_INFO")])
>>> playlist = xspf.Playlist(title="Some Tracks",
                             creator="myself",
                             annotation="I did this only for examples!.",
                             trackList=[killer_queen, anbtd])
>>> print(playlist.xml_string())
<playlist version="1" xmlns="http://xspf.org/ns/0/"><title>Some Tracks</title><creator>myself</creator><annotation>I did this only for examples!.</annotation><date>2020-02-03T14:29:59.199202+03:00</date><trackList><track><location>file:///home/music/killer_queen.mp3</location><title>Killer Queen</title><creator>Queen</creator><annotation>#2 in GB 1975</annotation><info>https://ru.wikipedia.org/wiki/Killer_Queen</info><image>file:///home/images/killer_queen_cover.png</image><album>Sheer Heart Attack</album><trackNum>2</trackNum><duration>177000</duration></track><track><location>https://freemusic.example.com/loc.ogg</location><location>file:///home/music/anbtd.mp3</location><identifier>id1.group</identifier><title>Another One Bites the Dust</title><creator>Queen</creator><link rel="link.namespace">link.uri.info</link><meta rel="meta.namespace">METADATA_INFO</meta></track></trackList></playlist>
>>> playlist.write("some_tracks.xspf")

2. Parsing from file.

>>> from xspf_lib import Playlist
>>> playlist = Playlist.parse("some_tracks.xspf")

License
-------

The license of the project is MIT License - see LICENSE_ file for details.

.. _LICENSE: https://github.com/dem214/xspf-lib/blob/master/LICENSE

.. _pip: https://pip.pypa.io/en/stable/quickstart
