import shopify_api
from test.test_helper import TestCase
from pyactiveresource.activeresource import ActiveResource
from mock import patch
import threading

class BaseTest(TestCase):

    @classmethod
    def setUpClass(self):
        shopify_api.ApiVersion.define_known_versions()
        shopify_api.ApiVersion.define_version(shopify_api.Release('2019-04'))
        self.session1 = shopify_api.Session('shop1.myshopify.com', 'unstable', 'token1')
        self.session2 = shopify_api.Session('shop2.myshopify.com', '2019-04', 'token2')

    @classmethod
    def tearDownClass(self):
        shopify_api.ApiVersion.clear_defined_versions()

    def setUp(self):
        super(BaseTest, self).setUp()

    def tearDown(self):
        shopify_api.ShopifyResource.clear_session()

    def test_activate_session_should_set_site_and_headers_for_given_session(self):
        shopify_api.ShopifyResource.activate_session(self.session1)

        self.assertIsNone(ActiveResource.site)
        self.assertEqual('https://shop1.myshopify.com/admin/api/unstable', shopify_api.ShopifyResource.site)
        self.assertEqual('https://shop1.myshopify.com/admin/api/unstable', shopify_api.Shop.site)
        self.assertIsNone(ActiveResource.headers)
        self.assertEqual('token1', shopify_api.ShopifyResource.headers['X-Shopify-Access-Token'])
        self.assertEqual('token1', shopify_api.Shop.headers['X-Shopify-Access-Token'])

    def test_activate_session_should_set_site_given_version(self):
        shopify_api.ShopifyResource.activate_session(self.session2)

        self.assertIsNone(ActiveResource.site)
        self.assertEqual('https://shop2.myshopify.com/admin/api/2019-04', shopify_api.ShopifyResource.site)
        self.assertEqual('https://shop2.myshopify.com/admin/api/2019-04', shopify_api.Shop.site)
        self.assertIsNone(ActiveResource.headers)

    def test_clear_session_should_clear_site_and_headers_from_Base(self):
        shopify_api.ShopifyResource.activate_session(self.session1)
        shopify_api.ShopifyResource.clear_session()

        self.assertIsNone(ActiveResource.site)
        self.assertIsNone(shopify_api.ShopifyResource.site)
        self.assertIsNone(shopify_api.Shop.site)

        self.assertIsNone(ActiveResource.headers)
        self.assertFalse('X-Shopify-Access-Token' in shopify_api.ShopifyResource.headers)
        self.assertFalse('X-Shopify-Access-Token' in shopify_api.Shop.headers)

    def test_activate_session_with_one_session_then_clearing_and_activating_with_another_session_shoul_request_to_correct_shop(self):
        shopify_api.ShopifyResource.activate_session(self.session1)
        shopify_api.ShopifyResource.clear_session()
        shopify_api.ShopifyResource.activate_session(self.session2)

        self.assertIsNone(ActiveResource.site)
        self.assertEqual('https://shop2.myshopify.com/admin/api/2019-04', shopify_api.ShopifyResource.site)
        self.assertEqual('https://shop2.myshopify.com/admin/api/2019-04', shopify_api.Shop.site)

        self.assertIsNone(ActiveResource.headers)
        self.assertEqual('token2', shopify_api.ShopifyResource.headers['X-Shopify-Access-Token'])
        self.assertEqual('token2', shopify_api.Shop.headers['X-Shopify-Access-Token'])

    def test_delete_should_send_custom_headers_with_request(self):
        shopify_api.ShopifyResource.activate_session(self.session1)

        org_headers=shopify_api.ShopifyResource.headers
        shopify_api.ShopifyResource.set_headers({'X-Custom': 'abc'})

        with patch('shopify_api.ShopifyResource.connection.delete') as mock:
            url = shopify_api.ShopifyResource._custom_method_collection_url('1', {})
            shopify_api.ShopifyResource.delete('1')
            mock.assert_called_with(url, {'X-Custom': 'abc'})

        shopify_api.ShopifyResource.set_headers(org_headers)

    def test_headers_includes_user_agent(self):
        self.assertTrue('User-Agent' in shopify_api.ShopifyResource.headers)
        t = threading.Thread(target=lambda: self.assertTrue('User-Agent' in shopify_api.ShopifyResource.headers))
        t.start()
        t.join()

    def test_headers_is_thread_safe(self):
        def testFunc():
            shopify_api.ShopifyResource.headers['X-Custom'] = 'abc'
            self.assertTrue('X-Custom' in shopify_api.ShopifyResource.headers)

        t1 = threading.Thread(target=testFunc)
        t1.start()
        t1.join()

        t2 = threading.Thread(target=lambda: self.assertFalse('X-Custom' in shopify_api.ShopifyResource.headers))
        t2.start()
        t2.join()

    def test_setting_with_user_and_pass_strips_them(self):
        shopify_api.ShopifyResource.clear_session()
        self.fake(
            'shop',
            url='https://this-is-my-test-show.myshopify.com/admin/shop.json',
            method='GET',
            body=self.load_fixture('shop'),
            headers={'Authorization': u'Basic dXNlcjpwYXNz'}
        )
        API_KEY = 'user'
        PASSWORD = 'pass'
        shop_url = "https://%s:%s@this-is-my-test-show.myshopify.com/admin" % (API_KEY, PASSWORD)
        shopify_api.ShopifyResource.set_site(shop_url)
        res = shopify_api.Shop.current()
        self.assertEqual('Apple Computers', res.name)
