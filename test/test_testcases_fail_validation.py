from xspf_lib import Playlist, Track, Extension
import os
import pytest


def get_testfile(path):
    return os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)),
        *['testcase', 'version_1', 'fail', path])


def test_playlist_attribute_forbidden_annotation():
    print(os.getcwd())
    pl = Playlist.parse(get_testfile(
        'playlist-attribute-forbidden-annotation.xspf'))
    raise NotImplementedError


def test_playlist_attribute_forbidden_playlist():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile(
            'playlist-attribute-forbidden-playlist.xspf'))


def test_playlist_baddate():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile(
            "playlist-baddate.xspf"))


def test_playlist_badversion():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile(
            "playlist-badversion.xspf"))


def test_playlist_broken_relative_path():
    Playlist.parse(get_testfile("playlist-broken-relative-paths.xspf"))
    raise NotImplementedError("is it realy must to fail?")


def test_playlist_element_forbidden_attributution():
    pl = Playlist.parse(get_testfile(
        "playlist-element-forbidden-attribution.xspf"
    ))
    raise NotImplementedError()


def test_playlist_extension_application_missing():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile(
            "playlist-extension-application-missing.xspf"
        ))


def test_playlist_link_rel_missing():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile(
            "playlist-link-rel-missing.xspf"
        ))


def test_playlist_markup_annotation():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile(
            "playlist-markup-annotation.xspf"
        ))


def test_playlist_markup_creator():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile(
            "playlist-markup-creator.xspf"
        ))


def test_playlist_markup_meta():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile(
            "playlist-markup-meta.xspf"
        ))


def test_playlist_markup_title():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile(
            "playlist-markup-title.xspf"
        ))


def test_playlist_meta_rel_missing():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile(
            "playlist-meta-rel-missing.xspf"
        ))
