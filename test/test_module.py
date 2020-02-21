from xspf_lib import Track, Playlist, Extension, Link, Meta, Attribution
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as ET
from datetime import datetime


def test_track_init():
    tr = Track(location="here.mp3",
               identifier="id",
               title="tr_title",
               creator="tr_creator",
               annotation="comment",
               info="info.example.com",
               album="tr_album",
               trackNum="1",
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
