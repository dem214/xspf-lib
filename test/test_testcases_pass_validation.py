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
    assert pl.extension[0].get("application") == \
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
    assert "extension" in pl.extension[0].tag
    # TODO: Add extension assertion
    assert len(pl.extension) == 1
    assert len(pl.trackList) == 0
