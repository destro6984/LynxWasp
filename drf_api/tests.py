from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from product_manager_ices.models import Flavour, Ices, Order
from product_manager_ices.tests import IceCreamTestData


class IceCreamTestAPIData(APITestCase, IceCreamTestData):
    pass


class IceApiViewTest(IceCreamTestAPIData):
    def setUp(self):
        self.url = reverse("ices")

    def test_list_not_logged(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_create_not_superuser(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create(self):
        self.client.force_authenticate(user=self.admin_user)

        self.assertEqual(Ices.objects.all().count(), 2)
        response = self.client.post(reverse("ices"), data={"type": "test", "price": 12})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Ices.objects.all().count(), 3)

    def test_create_wrong_input(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post(self.url, data={"type": "scoope", "price": 15.5})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class FlavourApiViewTest(IceCreamTestAPIData):
    def setUp(self):
        self.url = reverse("flavours")

    def test_list_not_logged(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)

    def test_create(self):
        self.client.force_authenticate(user=self.test_user)

        self.assertEqual(Flavour.objects.all().count(), 4)
        response = self.client.post(self.url, data={"flavour": "coconut"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Flavour.objects.all().count(), 5)

    def test_create_wrong_input(self):
        self.client.force_authenticate(user=self.test_user)

        response = self.client.post(self.url, data={"flavour": "chocolate"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OrderListApiViewTest(IceCreamTestAPIData):
    def setUp(self):
        self.url = reverse("order-list")

    def test_list_not_logged(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list(self):
        self.client.force_authenticate(user=self.test_user)
        Order.objects.create(worker_owner=self.test_user, status=Order.Status.STARTED)
        response = self.client.get(f"{self.url}?q=tester1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)


class OrderCreateApiViewTest(IceCreamTestAPIData):
    def setUp(self):
        self.url = reverse("order-create")


class OrderRetrieveUpdateDestroyAPIViewTest(IceCreamTestAPIData):
    def setUp(self):
        self.url = reverse("order-manage")
