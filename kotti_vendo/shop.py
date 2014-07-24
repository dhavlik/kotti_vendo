#coding:utf8
from kotti.resources import Content, Image
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Unicode
from sqlalchemy import Numeric
from sqlalchemy import Text

from kotti_vendo import _


class VendoShop(Content):
    """My content type"""

    id = Column(
        Integer(),
        ForeignKey('contents.id'),
        primary_key=True)

    # Prefix for order numbers
    prefix = Column(
        Unicode())

    type_info = Content.type_info.copy(
        name=u'VendoShop',
        title=_(u'Shop'),
        add_view=u'add_vendoshop',
        addable_to=['Document', ],)

    def __init__(self, prefix=u"", **kwargs):
        super(VendoShop, self).__init__(**kwargs)
        self.prefix = prefix


Image.type_info.addable_to.append('VendoProduct')


class VendoProduct(Content):
    """Sellable product"""

    id = Column(
        Integer(),
        ForeignKey('contents.id'),
        primary_key=True)

    # Stock keeping unit id
    sku = Column(Text(), unique=True)
    variation_title = Column(Text())

    type_info = Content.type_info.copy(
        name=u'VendoProduct',
        title=_(u'Product'),
        add_view=u'add_vendoproduct',
        addable_to=['VendoShop'],)

    def __init__(self, sku=u"", **kwargs):
        super(VendoProduct, self).__init__(**kwargs)
        self.sku = sku

    def images(self, request):
        """REturns url to images in this container"""
        all_children = self.children_with_permission(request)
        index = 0
        for child in all_children:
            if isinstance(child, Image):
                yield dict(url=request.resource_url(child),
                           title=child.title, index=index)
                index += 1

    def variations(self, request):
        """REturns all variations of this product"""
        all_children = self.children_with_permission(request)
        for child in all_children:
            if isinstance(child, VendoProductVariation):
                yield child


class VendoProductVariation(Content):
    """Variation of a product"""

    id = Column(
        Integer(),
        ForeignKey('contents.id'),
        primary_key=True)

    sub_sku = Column(Text())
    default_price = Column(Numeric())
    unit_singular = Column(Text())
    unit_plural = Column(Text())

    type_info = Content.type_info.copy(
        name=u'VendoProductVariation',
        title=_(u'Product Variation'),
        add_view=u'add_vendoproductvariation',
        addable_to=['VendoProduct', ],)

    def __init__(self, **kw):
        super(VendoProductVariation, self).__init__(**kw)
        self.sub_sku = kw.get('sub_sku', '')
        self.default_price = kw.get('default_price', 0.0)
        self.unit_singular = kw.get('unit_singular', '')
        self.unit_plural = kw.get('unit_plural', '')

    def formatted_price(self):
        return u'%.2d €' % self.default_price
