import shopify_api
from test.test_helper import TestCase

class PublicationTest(TestCase):
    def test_find_all_publications(self):
        self.fake('publications')
        publications = shopify_api.Publication.find()

        self.assertEqual(55650051, publications[0].id)
        self.assertEqual("Buy Button", publications[0].name)
