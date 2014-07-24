from kotti.resources import get_root

from kotti_vendo.shop import VendoShop
from kotti_vendo.views import VendoShopView


def test_views(db_session, dummy_request):

    root = get_root()
    content = VendoShop()
    root['content'] = content

    view = VendoShopView(root['content'], dummy_request)

    assert view.view() == {}
    assert view.alternative_view() == {}
