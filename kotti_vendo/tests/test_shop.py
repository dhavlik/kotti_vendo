from kotti.resources import get_root
from kotti.testing import DummyRequest

from kotti_vendo.shop import VendoShop


def test_vendoshop(db_session):

    root = get_root()
    content = VendoShop()
    assert content.type_info.addable(root, DummyRequest()) is True
    root['content'] = content
