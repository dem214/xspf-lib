from xspf_lib import Track
from xml.etree.ElementTree import Element


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
