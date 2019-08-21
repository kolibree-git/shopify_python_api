import shopify_api
from test.test_helper import TestCase

class ApiPermissionTest(TestCase):

    def test_delete_api_permission(self):
        self.fake(
            'api_permissions/current',
            method='DELETE',
            code=200,
            body='{}'
        )

        shopify_api.ApiPermission.delete()
