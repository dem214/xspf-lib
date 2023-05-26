"""Module helps to work with xspf playlists."""

__all__ = ["Playlist", "Track", "Attribution", "Extension", "Link", "Meta", "URI"]
import xml.etree.ElementTree as Et

from ._version import __version__  # noqa: F401 unused but used
from .constants import XML_NAMESPACE
from .elements import Attribution, Extension, Link, Meta, Playlist, Track
from .types import URI

Et.register_namespace("", XML_NAMESPACE["xspf"])
