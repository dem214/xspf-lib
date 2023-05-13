import xspf_lib
import xspf_lib.elements


def test_youtube_case():
    t = xspf_lib.elements.Track("https://youtube.com/watch?v=[id]")
    assert (
        t.xml_string()
        == "<track><location>https://youtube.com/watch?v=[id]</location></track>"
    )
