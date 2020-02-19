from xspf_lib import Playlist
import os
from datetime import datetime, timezone, timedelta

testcase_dir = os.path.join(
    os.path.dirname(
        os.path.abspath(__file__)),
    *['testcase', 'version_1', 'pass'])

os.chdir(testcase_dir)


def test_playlist_empty_annotation():
    Playlist.parse("playlist-empty-annotation.xspf")


def test_playlist_empty_creator():
    Playlist.parse("playlist-empty-creator.xspf")


def test_track_whitespace_int():
    pl = Playlist.parse("track-whitespace-nonNegativeInteger.xspf")
    for i in range(4):
        assert pl[i].duration == 1


def test_playlist_empty_title():
    Playlist.parse("playlist-empty-title.xspf")


def test_playlist_empty_meta():
    Playlist.parse("playlist-empty-meta.xspf")


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
    assert pl.identifier == \
        "magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE52SJUQCZO5C"
    assert pl.image == "http://example.com/img/mypicture"
    assert pl.date == datetime(2005, 1, 8, 17, 10, 47,
                               tzinfo=timezone(timedelta(hours=-5)))
    assert pl.license == "http://creativecommons.org/licenses/by/1.0/"
    assert len(pl.attribution) == 2
    assert pl.attribution[0].identifier == "http://bar.com/secondderived.xspf"
    assert pl.attribution[1].location == "http://foo.com/original.xspf"
    assert pl.link[0].rel == "http://foaf.example.org/namespace/version1"
    assert pl.link[0].content == \
        "http://socialnetwork.example.org/foaf/mary.rdfs"
    assert len(pl.link) == 1
    assert pl.meta[0].rel == "http://example.org/key"
    assert pl.meta[0].content == "value"
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
    assert pl.link[0].rel == "http://example.com/"
    assert pl.link[0].content == "http://example.com/"
    assert len(pl.link) == 2
    assert pl.meta[0].rel == "http://example.com/"
    assert pl.meta[0].content == "value"
    assert len(pl.meta) == 2
    assert pl.extension[0].application == 'http://example.com/'
    assert len(pl.extension) == 2
    assert len(pl.trackList) == 0


def test_playlist_namespace_nested_proper():
    pl = Playlist.parse('playlist-namespace-nested-proper.xspf')
    assert pl.extension[0].application == "http://example.com/"


def test_playlist_namespace_nondefault():
    Playlist.parse('playlist-namespace-nondefault.xspf')


def test_playlist_namespace_two_additions():
    Playlist.parse("playlist-namespace-two-additions.xspf")


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


def test_track_extensive():
    tr = Playlist.parse("track-extensive.xspf")[0]
    assert len(tr.location) == 1
    assert tr.location[0] == "http://example.com/my.mp3"
    assert len(tr.identifier) == 1
    assert tr.identifier[0] == \
        "magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE52SJUQCZO5C"
    assert tr.title == "My Way"
    assert tr.creator == "Frank Sinatra"
    assert tr.annotation == "This is my theme song."
    assert tr.info == "http://franksinatra.com/myway"
    assert tr.image == "http://franksinatra.com/img/myway"
    assert tr.album == "Frank Sinatra's Greatest Hits"
    assert tr.trackNum == 3
    assert tr.duration == 19200
    assert len(tr.link) == 1
    assert tr.link[0].rel == "http://foaf.org/namespace/version1"
    assert tr.link[0].content == "http://socialnetwork.org/foaf/mary.rdfs"
    assert len(tr.meta) == 1
    assert tr.meta[0].rel == "http://example.org/key"
    assert tr.meta[0].content == "value"
    assert len(tr.extension) == 1
    assert tr.extension[0].application == "http://example.com"


def test_track_inverted_order():
    tr = Playlist.parse("track-inverted-order.xspf")[0]
    assert len(tr.location) == 1
    assert tr.location[0] == "http://example.com/"
    assert len(tr.identifier) == 1
    assert tr.identifier[0] == "http://example.com/"
    assert tr.title == "some text"
    assert tr.creator == "some text"
    assert tr.annotation == "some text"
    assert tr.info == "http://example.com/"
    assert tr.image == "http://example.com/"
    assert tr.trackNum == 2
    assert tr.duration == 120000
    assert len(tr.link) == 2
    assert all(link.rel == "http://example.com/" for link in tr.link)
    assert all(link.content == "http://example.com/" for link in tr.link)
    assert len(tr.meta) == 2
    assert all(meta.rel == "http://example.com/" for meta in tr.meta)
    assert all(meta.content == "value" for meta in tr.meta)
    assert len(tr.extension) == 2
    assert all(extension.application == "http://example.com/"
               for extension in tr.extension)


def test_track_whitespace_anyURI():
    tr = Playlist.parse("track-whitespace-anyURI.xspf")[0]
    assert len(tr.location) == 4
    assert tr.location[0] == "http://example.com/no_whitespace/"
    assert tr.location[1] == "http://example.com/whitespace_before/"
    assert tr.location[2] == "http://example.com/whitespace_after/"
    assert tr.location[3] == "http://example.com/whitespace_before_and_after/"


def test_track_whitespace_nonNegativeInteger():
    pl = Playlist.parse("track-whitespace-nonNegativeInteger.xspf")
    assert len(pl) == 4
    for tr in pl:
        assert tr.duration == 1
