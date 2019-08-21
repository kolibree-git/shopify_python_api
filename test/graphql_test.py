import shopify_api
import json
from test.test_helper import TestCase

class GraphQLTest(TestCase):

    def setUp(self):
        super(GraphQLTest, self).setUp()
        shopify_api.ApiVersion.define_known_versions()
        shopify_session = shopify_api.Session('this-is-my-test-show.myshopify.com', 'unstable', 'token')
        shopify_api.ShopifyResource.activate_session(shopify_session)
        client = shopify_api.GraphQL()
        self.fake(
            'graphql', 
            method='POST', 
            code=201, 
            headers={
                'X-Shopify-Access-Token': 'token',
                'Accept': 'application/json', 
                'Content-Type': 'application/json'
                })
        query = '''
            {
                shop {
                    name
                    id
                }
            }
        '''
        self.result = client.execute(query)


    def test_fetch_shop_with_graphql(self):
        self.assertTrue(json.loads(self.result)['shop']['name'] == 'Apple Computers')