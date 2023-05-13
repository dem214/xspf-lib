# URI checker By RFC 3986
lowalpha = "abcdefghijklmnopqrstuvwxyz"
upalpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
alpha = lowalpha + upalpha
digit = "0123456789"
unreserved = alpha + digit + "-._~"
gen_delims = ":/?#[]@"
sub_delims = "!$&'()*+,;="
reserved = gen_delims + sub_delims
quoted = "%"
URI_CHARACTERS = reserved + unreserved + quoted

XML_NAMESPACE = {"xspf": "http://xspf.org/ns/0/"}
