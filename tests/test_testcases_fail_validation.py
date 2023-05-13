from pathlib import Path

import pytest

from xspf_lib import Link, Meta, Playlist

TESTCASE_DIR: Path = (
    Path(__file__).absolute().parent / "testcase" / "version_1" / "fail"
)


def get_testcase_path(filename):
    return TESTCASE_DIR / filename


failed_templates = [
    ("playlist-attribute-forbidden-annotation.xspf", TypeError),
    ("playlist-attribute-forbidden-playlist.xspf", TypeError),
    ("playlist-baddate.xspf", ValueError),
    ("playlist-badversion.xspf", ValueError),
    ("playlist-element-forbidden-attribution.xspf", TypeError),
    ("playlist-extension-application-missing.xspf", TypeError),
    ("playlist-link-rel-missing.xspf", TypeError),
    ("playlist-markup-annotation.xspf", ValueError),
    ("playlist-markup-creator.xspf", ValueError),
    ("playlist-markup-meta.xspf", ValueError),
    ("playlist-markup-title.xspf", ValueError),
    ("playlist-meta-rel-missing.xspf", TypeError),
    ("playlist-missingtracklist.xspf", TypeError),
    ("playlist-missingversion.xspf", TypeError),
    ("playlist-namespace-missing.xspf", TypeError),
    ("playlist-namespace-wrong-string.xspf", ValueError),
    ("playlist-nonleaf-content-attribution.xspf", TypeError),
    ("playlist-nonleaf-content-playlist.xspf", TypeError),
    ("playlist-nonleaf-content-trackList.xspf", TypeError),
    ("playlist-root-name.xspf", ValueError),
    ("playlist-toomany-annotation.xspf", TypeError),
    ("playlist-toomany-attribution.xspf", TypeError),
    ("playlist-toomany-creator.xspf", TypeError),
    ("playlist-toomany-date.xspf", TypeError),
    ("playlist-toomany-identifier.xspf", TypeError),
    ("playlist-toomany-image.xspf", TypeError),
    ("playlist-toomany-info.xspf", TypeError),
    ("playlist-toomany-license.xspf", TypeError),
    ("playlist-toomany-location.xspf", TypeError),
    ("playlist-toomany-title.xspf", TypeError),
    ("playlist-toomany-tracklist.xspf", TypeError),
    ("track-badint-duration.xspf", ValueError),
    ("track-badint-tracknum.xspf", ValueError),
    ("track-extension-application-missing.xspf", TypeError),
    ("track-link-rel-missing.xspf", TypeError),
    ("track-markup-album.xspf", ValueError),
    ("track-markup-annotation.xspf", ValueError),
    ("track-markup-creator.xspf", ValueError),
    ("track-markup-meta.xspf", ValueError),
    ("track-markup-title.xspf", ValueError),
    ("track-meta-rel-missing.xspf", TypeError),
    ("track-nonleaf-content.xspf", TypeError),
    ("track-toomany-album.xspf", TypeError),
    ("track-toomany-annotation.xspf", TypeError),
    ("track-toomany-creator.xspf", TypeError),
    ("track-toomany-duration.xspf", TypeError),
    ("track-toomany-image.xspf", TypeError),
    ("track-toomany-info.xspf", TypeError),
    ("track-toomany-title.xspf", TypeError),
    ("track-toomany-tracknum.xspf", TypeError),
]


@pytest.mark.parametrize("filename,exc", failed_templates)
def test_corrupted_playlist(filename: str, exc: Exception):
    with pytest.raises(exc):
        Playlist.parse(get_testcase_path(filename))


def test_also_playlist_creation_without_link_rel():
    with pytest.raises(TypeError):
        Playlist(link=[Link(content="file:/let_me_in")])


def test_also_playlist_creation_without_meta_rel():
    with pytest.raises(TypeError):
        Playlist(meta=[Meta(content="imma content")])


def test_also_playlist_create_empty_tracklist_element():
    assert "<trackList />" in Playlist().xml_string()


def test_also_playlist_create_version_attribute():
    assert 'version="1"' in Playlist().xml_string()
