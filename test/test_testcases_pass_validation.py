from xspf_lib import Playlist, Track, Extension
import os
from datetime import datetime, timezone, timedelta
import xml.etree.ElementTree as ET

testcase_dir = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)),
    *['testcase', 'version_1', 'pass'])

os.chdir(testcase_dir)

def test_playlist_empty_annotation():
    pl = Playlist.parse("playlist-empty-annotation.xspf")

def test_playlist_empty_creator():
    pl = Playlist.parse("playlist-empty-creator.xspf")

def test_track_whitespace_int():
    pl = Playlist.parse("track-whitespace-nonNegativeInteger.xspf")
    for i in range(4):
        assert pl[i].duration == 1

def test_playlist_empty_title():
    pl = Playlist.parse("playlist-empty-title.xspf")

def test_playlist_empty_meta():
    pl = Playlist.parse("playlist-empty-meta.xspf")

def test_playlist_extension():
    pl = Playlist.parse("playlist-extension.xspf")
    assert pl.extension[0].application == \
        "http://localhost/some/valid/url"
    # TODO: assert something

def test_playlist_extensive():
    pl = Playlist.parse("playlist-extensive.xspf")
    assert pl.title == "My playlist"
    assert pl.creator == "Jane Doe"
    assert pl.annotation == "My favorite songs"
    assert pl.info == "http://example.com/myplaylists"
    assert pl.location == "http://example.com/myplaylists/myplaylist"
    assert pl.identifier == "magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE52SJUQCZO5C"
    assert pl.image == "http://example.com/img/mypicture"
    assert pl.date == datetime(2005, 1, 8, 17, 10, 47,
                               tzinfo=timezone(timedelta(hours=-5)))
    assert pl.license == "http://creativecommons.org/licenses/by/1.0/"
    # TODO: check attribution
    assert pl.link[0] == ("http://foaf.example.org/namespace/version1",
                          "http://socialnetwork.example.org/foaf/mary.rdfs")
    assert len(pl.link) == 1
    assert pl.meta[0] == ("http://example.org/key", "value")
    assert len(pl.meta) == 1
    # TODO: Add extension assertion
    assert len(pl.extension) == 1
    assert pl.extension[0].application == "http://example.com"
    assert len(pl.trackList) == 0

def test_playlist_inverted_order():
    pl = Playlist.parse("playlist-inverted-order.xspf")
    assert pl.title == "some text"
    assert pl.creator == "some text"
    assert pl.annotation == "some text"
    assert pl.info == "http://example.com/"
    assert pl.location == "http://example.com/"
    assert pl.identifier == "http://example.com/"
    assert pl.image == "http://example.com/"
    assert pl.date == datetime(2005, 1, 8, 17, 10, 47,
                               tzinfo=timezone(timedelta(hours=-5)))
    assert pl.license == "http://example.com/"
    # TODO: check attribution
    assert pl.link[0] == ("http://example.com/",
                          "http://example.com/")
    assert len(pl.link) == 2
    assert pl.meta[0] == ("http://example.com/", "value")
    assert len(pl.meta) == 2
    assert pl.extension[0].application == 'http://example.com/'
    assert len(pl.extension) == 2
    assert len(pl.trackList) == 0

def test_playlist_namespace_nested_proper():
    pl = Playlist.parse('playlist-namespace-nested-proper.xspf')
    assert pl.extension[0].application == "http://example.com/"

def test_playlist_namespace_nondefault():
    pl = Playlist.parse('playlist-namespace-nondefault.xspf')

def test_playlist_namespace_two_additions():
    pl = Playlist.parse("playlist-namespace-two-additions.xspf")

def test_playlist_relative_paths():
    pl = Playlist.parse("playlist-relative-paths.xspf")
    assert pl[0].location[0] == "../01-Ain't Mine.flac"
    assert pl[0].title == "Ain't Mine"
    assert pl[1].location[0] == "02-Solitude over the River.flac"
    assert pl[1].title == "Solitude over the River"
    assert pl[2].location[0] == "./03-Jack Man.flac"
    assert pl[2].title == "Jack Man"

def test_playlist_whitespace_dateTime():
    pl = Playlist.parse("playlist-whitespace-dateTime.xspf")
    assert pl.date == datetime(2005, 1, 8, 17, 10, 47,
                               tzinfo=timezone(timedelta(hours=-5)))

def test_playlist_xml_base():
    Playlist.parse("playlist-xml-base.xspf")

def test_track_empty_album():
    Playlist.parse("track-empty-album.xspf")

def test_track_empty_annotation():
    Playlist.parse("track-empty-creator.xspf")

def test_track_empty_meta():
    Playlist.parse("track-empty-meta.xspf")

def test_track_empty_title():
    Playlist.parse("track-empty-title.xspf")

def test_track_extension():
    tr = Playlist.parse("track-extension.xspf")[0]
    assert tr.extension[0].application == "http://localhost/some/valid/url"
    assert len(tr.extension) == 1
    assert len(tr.extension[0].content) == 2
