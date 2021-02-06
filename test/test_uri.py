import xspf_lib

def test_youtube_case():
    t = xspf_lib.Track('https://youtube.com/watch?v=[id]')
    assert t.xml_string() == '<track><location>https://youtube.com/watch?v=[id]</location></track>'