from pyramid.i18n import TranslationStringFactory
from kotti.views.slots import assign_slot

_ = TranslationStringFactory('kotti_vendo')


def kotti_configure(settings):
    settings['pyramid.includes'] += ' kotti_vendo'
    vendotypes = (
        'kotti_vendo.shop.VendoShop',
        'kotti_vendo.shop.VendoProduct',
        'kotti_vendo.shop.VendoProductVariation',)
    settings['kotti.available_types'] += ' ' + ' '.join(vendotypes)
    assign_slot('cart', 'abovecontent')


def includeme(config):
    config.add_translation_dirs('kotti_vendo:locale')
    config.scan(__name__)
