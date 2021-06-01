
from push_api_clientpy import DocumentBuilder
import pytest

def test_docbuilder():
    assert DocumentBuilder("https://foo.com", "the_title").marshal().get('uri') == "https://foo.com"