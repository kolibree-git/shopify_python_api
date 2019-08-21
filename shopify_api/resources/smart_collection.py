from ..base import ShopifyResource
from shopify_api import mixins
import shopify_api


class SmartCollection(ShopifyResource, mixins.Metafields, mixins.Events):

    def products(self):
        return shopify_api.Product.find(collection_id=self.id)
