from ..base import ShopifyResource
from shopify_api import mixins


class Page(ShopifyResource, mixins.Metafields, mixins.Events):
    pass
