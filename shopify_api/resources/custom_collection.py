from ..base import ShopifyResource
from shopify_api import mixins
import shopify_api


class CustomCollection(ShopifyResource, mixins.Metafields, mixins.Events):

    def products(self):
        return shopify_api.Product.find(collection_id=self.id)

    def add_product(self, product):
        return shopify_api.Collect.create({'collection_id': self.id, 'product_id': product.id})

    def remove_product(self, product):
        collect = shopify_api.Collect.find_first(collection_id=self.id, product_id=product.id)
        if collect:
            collect.destroy()
