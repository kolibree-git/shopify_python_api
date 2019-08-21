from ..base import ShopifyResource
from shopify_api import mixins
import shopify_api

class Policy(ShopifyResource, mixins.Metafields, mixins.Events):
  pass
