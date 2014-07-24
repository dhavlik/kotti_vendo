# -*- coding: utf-8 -*-

from colander import SchemaNode
from colander import String, Decimal
from kotti.views.edit.content import ContentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from pyramid.view import view_config
from pyramid.view import view_defaults

from kotti_vendo import _
from kotti_vendo.shop import VendoShop, VendoProduct, VendoProductVariation
from kotti_vendo.fanstatic import kotti_vendo


class VendoShopSchema(ContentSchema):
    """Schema for add / edit forms of VendoShop"""

    prefix = SchemaNode(
        String(),
        title=_(u'Prefix'),
        missing=u"",
    )


@view_config(name=VendoShop.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt')
class VendoShopAddForm(AddFormView):

    schema_factory = VendoShopSchema
    add = VendoShop
    item_type = _(u"VendoShop")


@view_config(name='edit',
             context=VendoShop,
             permission='edit',
             renderer='kotti:templates/edit/node.pt')
class VendoShopEditForm(EditFormView):

    schema_factory = VendoShopSchema


@view_config(
    name='cart',
    renderer='kotti_vendo:templates/cart.pt')
class CartView(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        return {}

    def cartitems(self):
        return [
            dict(title=u'Blabla', price='12.99', amount='1', subtotal='12.99'),
            dict(title=u'Blubb', price='14.95', amount='1', subtotal='14.95')]


@view_config(
    name='cart_add',
    renderer='json')
class CartAdd(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        import pdb; pdb.set_trace()
        return {'message': 'added'}


@view_defaults(context=VendoShop, permission='view')
class VendoShopView(object):
    """View(s) for VendoShop"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(name='view',
                 renderer='kotti_vendo:templates/vendoshop.pt')
    def view(self):
        kotti_vendo.need()
        return {}


class VendoProductSchema(ContentSchema):
    """Schema for add / edit forms of VendoProduct"""

    sku = SchemaNode(
        String(),
        title=_(u'SKU'),
        missing=u"")

    variation_title = SchemaNode(
        String(),
        title=_(u'Variation title'),
        missing=u'')


@view_config(name=VendoProduct.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt')
class VendoProductAddForm(AddFormView):

    schema_factory = VendoProductSchema
    add = VendoProduct
    item_type = _(u"VendoProduct")


@view_config(name='edit',
             context=VendoProduct,
             permission='edit',
             renderer='kotti:templates/edit/node.pt')
class VendoProductEditForm(EditFormView):

    schema_factory = VendoProductSchema


@view_defaults(context=VendoProduct, permission='view')
class VendoProductView(object):
    """View(s) for VendoProduct"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(name='view',
                 renderer='kotti_vendo:templates/vendoproduct.pt')
    def view(self):
        kotti_vendo.need()
        return {}


class VendoProductVariationSchema(ContentSchema):
    """Schema for add / edit forms of VendoProductVariation"""

    sub_sku = SchemaNode(
        String(),
        title=_(u'Sub-SKU'),
        missing=u"")

    default_price = SchemaNode(
        Decimal(),
        title=_(u'Default price'))

    unit_singular = SchemaNode(
        String(),
        title=_(u'Unit name singular'))
    unit_plural = SchemaNode(
        String(),
        title=_(u'Unit name plural'))


@view_config(name=VendoProductVariation.type_info.add_view,
             permission='add',
             renderer='kotti:templates/edit/node.pt')
class VendoProductVariationAddForm(AddFormView):

    schema_factory = VendoProductVariationSchema
    add = VendoProductVariation
    item_type = _(u"VendoProductVariation")


@view_config(name='edit',
             context=VendoProductVariation,
             permission='edit',
             renderer='kotti:templates/edit/node.pt')
class VendoProductVariationEditForm(EditFormView):

    schema_factory = VendoProductVariationSchema


@view_defaults(context=VendoProductVariation, permission='view')
class VendoProductVariationView(object):
    """View(s) for VendoProductVariation"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    @view_config(name='view',
                 renderer='kotti_vendo:templates/VendoProductVariation.pt')
    def view(self):
        kotti_vendo.need()
        return {}
