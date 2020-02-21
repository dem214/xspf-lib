from xspf_lib import Playlist, Link, Meta
import os
import pytest


def get_testfile(path):
    return os.path.join(
        os.path.dirname(
            os.path.abspath(__file__)),
        *['testcase', 'version_1', 'fail', path])


def test_playlist_attribute_forbidden_annotation():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile(
            'playlist-attribute-forbidden-annotation.xspf'))


def test_playlist_attribute_forbidden_playlist():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile(
            'playlist-attribute-forbidden-playlist.xspf'))


def test_playlist_baddate():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-baddate.xspf"))


def test_playlist_badversion():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-badversion.xspf"))


def test_playlist_broken_relative_path():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-broken-relative-paths.xspf"))


def test_playlist_element_forbidden_attributution():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile(
            "playlist-element-forbidden-attribution.xspf"))


def test_playlist_extension_application_missing():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile(
            "playlist-extension-application-missing.xspf"
        ))


def test_playlist_link_rel_missing():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-link-rel-missing.xspf"))


def test_also_playlist_creation_without_link_rel():
    with pytest.raises(TypeError):
        Playlist(link=Link(content="file:/let_me_in"))


def test_playlist_markup_annotation():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-markup-annotation.xspf"))


def test_playlist_markup_creator():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-markup-creator.xspf"))


def test_playlist_markup_meta():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-markup-meta.xspf"))


def test_playlist_markup_title():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-markup-title.xspf"))


def test_playlist_meta_rel_missing():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-meta-rel-missing.xspf"))


def test_also_playlist_creation_without_meta_rel():
    with pytest.raises(TypeError):
        Playlist(meta=[Meta(content="imma content")])


def test_playlist_missing_tracklist():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-missingtracklist.xspf"))


def test_also_playlist_create_empty_tracklist_element():
    assert "<trackList />" in Playlist().xml_string()


def test_playlist_missing_version():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-missingversion.xspf"))


def test_also_playlist_create_version_attribute():
    assert 'version="1"' in Playlist().xml_string()


def test_playlist_namespase_missing():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-namespace-missing.xspf"))


# I didn't see any errors in `playlist-namespace-nested-broken.xspf` testcase


def test_playlist_namespace_wrong_string():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-namespace-wrong-string.xspf"))


def test_playlist_nonleaf_content_attribution():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile(
            "playlist-nonleaf-content-attribution.xspf"))


def test_playlist_nonleaf_content_playlist():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-nonleaf-content-playlist.xspf"))


def test_playlist_nonleaf_content_tracklist():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-nonleaf-content-trackList.xspf"))


def test_playlist_noturi_attribution_identifier():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile(
            "playlist-noturi-attribution-identifier.xspf"))


def test_playlist_noturi_attribution_location():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile(
            "playlist-noturi-attribution-location.xspf"))


def test_playlist_noturi_extension():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-noturi-extension.xspf"))


def test_playlist_noturi_identifier():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-noturi-identifier.xspf"))


def test_playlist_noturi_image():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-noturi-image.xspf"))


def test_playlist_noturi_info():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-noturi-info.xspf"))


def test_playlist_noturi_license():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-noturi-license.xspf"))


def test_playlist_noturi_link_content():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-noturi-link-content.xspf"))


def test_playlist_noturi_link_rel():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-noturi-link-rel.xspf"))


def test_playlist_noturi_location():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-noturi-location.xspf"))


def test_playlist_noturi_meta():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-noturi-meta.xspf"))


def test_playlist_root_name():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("playlist-root-name.xspf"))


def test_playlist_toomany_annotation():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-toomany-annotation.xspf"))


def test_playlist_toomany_attribution():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-toomany-attribution.xspf"))


def test_playlist_toomany_creator():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-toomany-creator.xspf"))


def test_playlist_toomany_date():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-toomany-date.xspf"))


def test_playlist_toomany_identifier():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-toomany-identifier.xspf"))


def test_playlist_toomany_image():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-toomany-image.xspf"))


def test_playlist_toomany_info():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-toomany-info.xspf"))


def test_playlist_toomany_license():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-toomany-license.xspf"))


def test_playlist_toomany_location():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-toomany-location.xspf"))


def test_playlist_toomany_title():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-toomany-title.xspf"))


def test_playlist_toomany_tracklist():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("playlist-toomany-tracklist.xspf"))


def test_track_badint_duration():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile('track-badint-duration.xspf'))


def test_track_badint_tracknum():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile('track-badint-tracknum.xspf'))


def test_track_extension_application_missing():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile(
            "track-extension-application-missing.xspf"))


def test_track_link_rel_missing():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("track-link-rel-missing.xspf"))


def test_track_markup_album():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("track-markup-album.xspf"))


def test_track_markup_annotation():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("track-markup-annotation.xspf"))


def test_track_markup_creator():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("track-markup-creator.xspf"))


def test_track_markup_meta():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("track-markup-meta.xspf"))


def test_track_markup_title():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("track-markup-title.xspf"))


def test_track_meta_rel_missing():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("track-meta-rel-missing.xspf"))


def test_track_nonleaf_content():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("track-nonleaf-content.xspf"))


def test_track_noturi_extension():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("track-noturi-extension.xspf"))


def test_track_noturi_identifier():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("track-noturi-identifier.xspf"))


def test_track_noturi_image():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("track-noturi-image.xspf"))


def test_track_noturi_info():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("track-noturi-info.xspf"))


def test_track_noturi_link_rel():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("track-noturi-link-rel.xspf"))


def test_track_noturi_location():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("track-noturi-location.xspf"))


def test_track_noturi_meta_rel():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile("track-noturi-meta-rel.xspf"))


def test_track_toomany_album():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("track-toomany-album.xspf"))


def test_track_toomany_annotation():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("track-toomany-annotation.xspf"))


def test_track_toomany_creator():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("track-toomany-creator.xspf"))


def test_track_toomany_duration():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("track-toomany-duration.xspf"))


def test_track_toomany_image():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("track-toomany-image.xspf"))


def test_track_toomany_info():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("track-toomany-info.xspf"))


def test_track_toomany_title():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("track-toomany-title.xspf"))


def test_track_toomany_tracknum():
    with pytest.raises(TypeError):
        Playlist.parse(get_testfile("track-toomany-tracknum.xspf"))


def test_track_whitespace_in_between():
    with pytest.raises(ValueError):
        Playlist.parse(get_testfile('track-whitespace-in-between.xspf'))
