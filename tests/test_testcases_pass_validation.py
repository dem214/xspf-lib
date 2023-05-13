from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import List

import pytest

from xspf_lib import Playlist

TESTCASE_DIR: Path = (
    Path(__file__).absolute().parent / "testcase" / "version_1" / "pass"
)


def get_testcase_path(filename: str) -> Path:
    return TESTCASE_DIR / filename


valid_playlists: List[str] = [
    "playlist-empty-annotation.xspf",
    "playlist-empty-creator.xspf",
    "playlist-empty-title.xspf",
    "playlist-empty-meta.xspf",
    "playlist-namespace-nondefault.xspf",
    "playlist-namespace-two-additions.xspf",
    "playlist-xml-base.xspf",
    "track-empty-album.xspf",
    "track-empty-creator.xspf",
    "track-empty-meta.xspf",
    "track-empty-title.xspf",
    "playlist-broken-relative-paths.xspf",
    "playlist-noturi-attribution-identifier.xspf",
    "playlist-noturi-attribution-location.xspf",
    "playlist-noturi-extension.xspf",
    "playlist-noturi-identifier.xspf",
    "playlist-noturi-image.xspf",
    "playlist-noturi-info.xspf",
    "playlist-noturi-license.xspf",
    "playlist-noturi-link-content.xspf",
    "playlist-noturi-link-rel.xspf",
    "playlist-noturi-location.xspf",
    "playlist-noturi-meta.xspf",
    "track-noturi-extension.xspf",
    "track-noturi-identifier.xspf",
    "track-noturi-image.xspf",
    "track-noturi-info.xspf",
    "track-noturi-link-rel.xspf",
    "track-noturi-location.xspf",
    "track-noturi-meta-rel.xspf",
    "track-whitespace-in-between.xspf",
]


@pytest.mark.parametrize("filename", valid_playlists)
def test_playlist_parse(filename: str):
    Playlist.parse(get_testcase_path(filename))


def test_track_whitespace_int():
    pl = Playlist.parse(get_testcase_path("track-whitespace-nonNegativeInteger.xspf"))
    for i in range(4):
        assert pl[i].duration == 1


def test_playlist_extension():
    pl = Playlist.parse(get_testcase_path("playlist-extension.xspf"))
    assert pl.extension[0].application == "http://localhost/some/valid/url"


def test_playlist_extensive():
    pl = Playlist.parse(get_testcase_path("playlist-extensive.xspf"))
    assert pl.title == "My playlist"
    assert pl.creator == "Jane Doe"
    assert pl.annotation == "My favorite songs"
    assert pl.info == "http://example.com/myplaylists"
    assert pl.location == "http://example.com/myplaylists/myplaylist"
    assert pl.identifier == "magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE52SJUQCZO5C"
    assert pl.image == "http://example.com/img/mypicture"
    assert pl.date == datetime(
        2005, 1, 8, 17, 10, 47, tzinfo=timezone(timedelta(hours=-5))
    )
    assert pl.license == "http://creativecommons.org/licenses/by/1.0/"
    assert len(pl.attribution) == 2
    assert pl.attribution[0].identifier == "http://bar.com/secondderived.xspf"
    assert pl.attribution[1].location == "http://foo.com/original.xspf"
    assert pl.link[0].rel == "http://foaf.example.org/namespace/version1"
    assert pl.link[0].content == "http://socialnetwork.example.org/foaf/mary.rdfs"
    assert len(pl.link) == 1
    assert pl.meta[0].rel == "http://example.org/key"
    assert pl.meta[0].content == "value"
    assert len(pl.meta) == 1
    # TODO: Add extension assertion
    assert len(pl.extension) == 1
    assert pl.extension[0].application == "http://example.com"
    assert len(pl.trackList) == 0


def test_playlist_inverted_order():
    pl = Playlist.parse(get_testcase_path("playlist-inverted-order.xspf"))
    assert pl.title == "some text"
    assert pl.creator == "some text"
    assert pl.annotation == "some text"
    assert pl.info == "http://example.com/"
    assert pl.location == "http://example.com/"
    assert pl.identifier == "http://example.com/"
    assert pl.image == "http://example.com/"
    assert pl.date == datetime(
        2005, 1, 8, 17, 10, 47, tzinfo=timezone(timedelta(hours=-5))
    )
    assert pl.license == "http://example.com/"
    # TODO: check attribution
    assert pl.link[0].rel == "http://example.com/"
    assert pl.link[0].content == "http://example.com/"
    assert len(pl.link) == 2
    assert pl.meta[0].rel == "http://example.com/"
    assert pl.meta[0].content == "value"
    assert len(pl.meta) == 2
    assert pl.extension[0].application == "http://example.com/"
    assert len(pl.extension) == 2
    assert len(pl.trackList) == 0


def test_playlist_namespace_nested_proper():
    pl = Playlist.parse(get_testcase_path("playlist-namespace-nested-proper.xspf"))
    assert pl.extension[0].application == "http://example.com/"


def test_playlist_relative_paths():
    pl = Playlist.parse(get_testcase_path("playlist-relative-paths.xspf"))
    assert pl[0].location[0] == "../01-Ain't Mine.flac"
    assert pl[0].title == "Ain't Mine"
    assert pl[1].location[0] == "02-Solitude over the River.flac"
    assert pl[1].title == "Solitude over the River"
    assert pl[2].location[0] == "./03-Jack Man.flac"
    assert pl[2].title == "Jack Man"


def test_playlist_whitespace_dateTime():
    pl = Playlist.parse(get_testcase_path("playlist-whitespace-dateTime.xspf"))
    assert pl.date == datetime(
        2005, 1, 8, 17, 10, 47, tzinfo=timezone(timedelta(hours=-5))
    )


def test_track_extension():
    tr = Playlist.parse(get_testcase_path("track-extension.xspf"))[0]
    assert tr.extension[0].application == "http://localhost/some/valid/url"
    assert len(tr.extension) == 1
    assert len(tr.extension[0].content) == 2


def test_track_extensive():
    tr = Playlist.parse(get_testcase_path("track-extensive.xspf"))[0]
    assert len(tr.location) == 1
    assert tr.location[0] == "http://example.com/my.mp3"
    assert len(tr.identifier) == 1
    assert tr.identifier[0] == "magnet:?xt=urn:sha1:YNCKHTQCWBTRNJIV4WNAE52SJUQCZO5C"
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
    tr = Playlist.parse(get_testcase_path("track-inverted-order.xspf"))[0]
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
    assert all(
        extension.application == "http://example.com/" for extension in tr.extension
    )


def test_track_whitespace_anyURI():
    tr = Playlist.parse(get_testcase_path("track-whitespace-anyURI.xspf"))[0]
    assert len(tr.location) == 4
    assert tr.location[0] == "http://example.com/no_whitespace/"
    assert tr.location[1] == "http://example.com/whitespace_before/"
    assert tr.location[2] == "http://example.com/whitespace_after/"
    assert tr.location[3] == "http://example.com/whitespace_before_and_after/"


def test_track_whitespace_nonNegativeInteger():
    pl = Playlist.parse(get_testcase_path("track-whitespace-nonNegativeInteger.xspf"))
    assert len(pl) == 4
    for tr in pl:
        assert tr.duration == 1
