from ..base import ShopifyResource
from shopify_api import mixins
import shopify_api


class Blog(ShopifyResource, mixins.Metafields, mixins.Events):

    def articles(self):
        return shopify_api.Article.find(blog_id=self.id)
