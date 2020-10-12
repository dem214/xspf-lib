import os

from xspf_lib import Track, Playlist, Extension, Link, Meta, Attribution
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
from datetime import datetime
import pytest


def test_track_init():
    tr = Track(location="here.mp3",
               identifier="id",
               title="tr_title",
               creator="tr_creator",
               annotation="comment",
               info="info.example.com",
               album="tr_album",
               trackNum=1,
               duration=10,
               link=[Link("link_type", "link_uri")],
               meta=[Meta("meta_type1", "metadata1"),
                     Meta("meta_type1", "metadata2")],
               extension=[Extension("appl",
                                    content=[Element('a', {'attr': "1"})])])
    resp = '<track>'\
        '<location>here.mp3</location>'\
        '<identifier>id</identifier>'\
        '<title>tr_title</title>'\
        '<creator>tr_creator</creator>'\
        '<annotation>comment</annotation>'\
        '<info>info.example.com</info>'\
        '<album>tr_album</album>'\
        '<trackNum>1</trackNum>'\
        '<duration>10</duration>'\
        '<link rel="link_type">link_uri</link>'\
        '<meta rel="meta_type1">metadata1</meta>'\
        '<meta rel="meta_type1">metadata2</meta>'\
        '<extension application="appl">'\
        '<a attr="1" />'\
        '</extension>'\
        '</track>'
    assert tr.xml_string() == resp


def test_playlist_init():
    pl = Playlist(title="That playlist",
                  creator="myself",
                  annotation="additional user info",
                  info="https://path_to_more.info",
                  location="file:///playlist.xspf",
                  identifier="this.playlist",
                  image="file:///default_cover.png",
                  license="CC",
                  attribution=[
                    Playlist(identifier="previous.playlist",
                             location="file:///last.playlist.xspf")],
                  link=[Link("link_type", "link_uri")],
                  meta=[Meta("meta_type1", "metadata1"),
                        Meta("meta_type1", "metadata2")],
                  extension=[Extension("appl",
                                       content=[
                                           Element('a', {'attr': "1"})])],
                  trackList=[Track(title="tr1"),
                             Track(title="tr2")])
    pl.date = datetime(2020, 4, 20, 12, 30, 1, 123456)
    response = '<playlist version="1" xmlns="http://xspf.org/ns/0/">'\
               '<title>That playlist</title>'\
               '<creator>myself</creator>'\
               '<annotation>additional user info</annotation>'\
               '<info>https://path_to_more.info</info>'\
               '<location>file:///playlist.xspf</location>'\
               '<identifier>this.playlist</identifier>'\
               '<image>file:///default_cover.png</image>'\
               '<date>2020-04-20T12:30:01.123456</date>'\
               '<license>CC</license>'\
               '<attribution>'\
               '<location>file:///last.playlist.xspf</location>'\
               '<identifier>previous.playlist</identifier>'\
               '</attribution>'\
               '<link rel="link_type">link_uri</link>'\
               '<meta rel="meta_type1">metadata1</meta>'\
               '<meta rel="meta_type1">metadata2</meta>'\
               '<extension application="appl">''<a attr="1" /></extension>'\
               '<trackList>'\
               '<track><title>tr1</title></track>'\
               '<track><title>tr2</title></track>'\
               '</trackList>'\
               '</playlist>'
    assert pl.xml_string() == response


def test_aattribution_xml_generator():
    atr = Attribution(location="file://ty", identifier="file://kylo")
    assert ['<location>file://ty</location>',
            '<identifier>file://kylo</identifier>'] == \
        [ET.tostring(el).decode() for el in atr.xml_elements()]
    atr_l = Attribution(location="file://ty")
    assert ['<location>file://ty</location>'] ==\
        [ET.tostring(el).decode() for el in atr_l.xml_elements()]
    atr_id = Attribution(identifier="file://id")
    assert ['<identifier>file://id</identifier>'] ==\
        [ET.tostring(el).decode() for el in atr_id.xml_elements()]
    atr_null = Attribution()
    assert len(list(atr_null.xml_elements())) == 0


def test_bad_trackNum_creation():
    with pytest.raises(ValueError):
        Track(trackNum=-1)


def test_bad_trackNum_assigment():
    tr = Track()
    with pytest.raises(ValueError):
        tr.trackNum = -1


def test_bad_trackNum_string():
    with pytest.raises(TypeError):
        Track(trackNum='1')


def test_bad_duration_creation():
    with pytest.raises(ValueError):
        Track(duration=-1)


def test_bad_duration_assignment():
    tr = Track()
    with pytest.raises(ValueError):
        tr.duration = -1


def test_bad_duration_string():
    with pytest.raises(TypeError):
        Track(duration='1')

def test_playlist_writing():
    import xspf_lib as xspf
    killer_queen = Track(location="file:///home/music/killer_queen.mp3",
                              title="Killer Queen",
                              creator="Queen",
                              album="Sheer Heart Attack",
                              trackNum=2,
                              duration=177000,
                              annotation="#2 in GB 1975",
                              info="https://ru.wikipedia.org/wiki/Killer_Queen",
                              image="file:///home/images/killer_queen_cover.png")
    anbtd = Track()
    anbtd.location = ["https://freemusic.example.com/loc.ogg",
                      "file:///home/music/anbtd.mp3"]
    anbtd.title = "Another One Bites the Dust"
    anbtd.creator = "Queen"
    anbtd.identifier = ["id1.group"]
    anbtd.link = [Link("link.namespace", "link.uri.info")]
    anbtd.meta = [Meta("meta.namespace", "METADATA_INFO")]
    playlist = Playlist(title="Some Tracks",
                             creator="myself",
                             annotation="I did this only for examples!.",
                             trackList=[killer_queen, anbtd])    
    playlist.date = datetime(2020, 4, 20, 12, 30, 1, 123456)
    playlist.write("some_tracks.xspf")
    with open('some_tracks.xspf', 'r') as file:
        playlist_xml = file.read()
    assert playlist_xml == '<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n'\
        '<playlist version="1" xmlns="http://xspf.org/ns/0/"><title>Some'\
        ' Tracks</title><creator>myself</creator><annotation>I did this '\
        'only for examples!.</annotation><date>2020-04-20T12:30:01.123456'\
        '</date><trackList><track><location>'\
        'file:///home/music/killer_queen.mp3</location><title>Killer Queen'\
        '</title><creator>Queen</creator><annotation>#2 in GB 1975'\
        '</annotation><info>https://ru.wikipedia.org/wiki/Killer_Queen'\
        '</info><image>file:///home/images/killer_queen_cover.png</image>'\
        '<album>Sheer Heart Attack</album><trackNum>2</trackNum><duration>'\
        '177000</duration></track><track><location>'\
        'https://freemusic.example.com/loc.ogg</location><location>'\
        'file:///home/music/anbtd.mp3</location><identifier>id1.group'\
        '</identifier><title>Another One Bites the Dust</title><creator>'\
        'Queen</creator><link rel="link.namespace">link.uri.info</link>'\
        '<meta rel="meta.namespace">METADATA_INFO</meta></track></trackList>'\
        '</playlist>'
    os.remove('some_tracks.xspf')
