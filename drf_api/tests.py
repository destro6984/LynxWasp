from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from product_manager_ices.tests import IceCreamTestData


class IceCreamTestAPIData(IceCreamTestData):
    pass


class IceApiViewTest(APITestCase, IceCreamTestData):
    def test_list(self):
        response = self.client.get(reverse("ices"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "scoope")
