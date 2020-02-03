from xspf_lib import Track, Playlist
from xml.etree.ElementTree import Element
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
               link=[("link_type", "link_uri")],
               meta=[("meta_type1", "metadata1"),
                     ("meta_type1", "metadata2")],
               extension=[("appl", Element('a', {'attr': "1"}))])
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
    pl = Playlist(title="that_playlist",
                  creator="myself",
                  annotation="additional user info",
                  info="https://path_to_more.info",
                  location="file:///playlist.xspf",
                  identifier="this.playlist",
                  image="file:///default_cover.png",
                  license="CC",
                  attribution=[Playlist(identifier="previous.playlist",
                                        location="file:///last.playlist.xspf")],
                  link=[("link_type", "link_uri")],
                  meta=[("meta_type1", "metadata1"),
                        ("meta_type1", "metadata2")],
                  extension=[("appl", Element('a', {'attr': "1"}))],
                  trackList=[Track(title="tr1"),
                             Track(title="tr2")])
    pl.date = datetime(2020, 4, 20, 12, 30, 1, 123456)
    response = '<playlist version="1" xmlns="http://xspf.org/ns/0/">'\
               '<title>that_playlist</title>'\
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
