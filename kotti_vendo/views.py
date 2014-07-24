# -*- coding: utf-8 -*-

from colander import SchemaNode
from colander import String, Decimal
from kotti.views.edit.content import ContentSchema
from kotti.views.form import AddFormView
from kotti.views.form import EditFormView
from kotti import DBSession
from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.httpexceptions import HTTPFound
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

    def _get_product(self, sku, subsku):
        """return tuple product & variation"""
        product = DBSession.query(
            VendoProduct).filter_by(sku=sku).one()
        variation = DBSession.query(
            VendoProductVariation).filter_by(sub_sku=subsku).one()
        return product, variation

    def total(self):
        total = 0
        cart = self.request.session.get('cart')
        if cart is None:
            return total
        for fullsku, cartitem in cart.items():
            product, variation = self._get_product(*fullsku.split('---'))
            total += variation.default_price * cartitem['amount']
        return total


    def cartitems(self):
        cart = self.request.session.get('cart')
        if cart is None:
            raise StopIteration
        for fullsku, cartitem in cart.items():
            product, variation = self._get_product(*fullsku.split('---'))
            yield dict(
                fullsku=fullsku,
                title=u'{} ({})'.format(product.title, variation.title),
                price=variation.default_price,
                amount=cartitem['amount'],
                subtotal=variation.default_price * cartitem['amount'])


class CartBase(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_cart(self):
        sess = self.request.session
        if 'cart' not in sess:
            cart = sess['cart'] = dict()
        else:
            cart = sess['cart']
        return cart

    def get_requested_full_sku(self):
        req = self.request.GET
        if 'fullsku' in req:
            return req['fullsku']
        sku = req['sku']
        subsku = req['sub']
        return '{}---{}'.format(sku, subsku)

    def go_back(self):
        cf = self.request.GET['cf']
        raise HTTPFound(location=cf)


@view_config(
    name='cart_remove',
    renderer='json')
class CartRemove(CartBase):

    def __call__(self):
        cart = self.get_cart()
        fullsku = self.get_requested_full_sku()
        del cart[fullsku]
        self.request.session.flash(
            'Successfully removed from cart.', 'success')
        self.go_back()


@view_config(
    name='cart_add',
    renderer='json')
class CartAdd(CartBase):

    def __call__(self):
        cart = self.get_cart()
        fullsku = self.get_requested_full_sku()
        if fullsku not in cart:
            cart[fullsku] = dict(amount=1)
        else:
            cart[fullsku]['amount'] += 1
        self.request.session.flash(
            'Successfully added to cart.', 'success')
        self.go_back()


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
