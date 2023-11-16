from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from product_manager_ices.models import Flavour, Ices, Order, OrderItem
from product_manager_ices.tests import IceCreamTestData


class IceCreamTestAPIData(APITestCase, IceCreamTestData):
    username2 = "tester2"
    email2 = "tester2@mail.com"
    password2 = "testing1234"
    last_name2 = "Iceman"
    first_name2 = "Ron"

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.test_user2 = get_user_model().objects.create_user(
            username=cls.username2,
            email=cls.email2,
            password=cls.password2,
            first_name=cls.first_name2,
            last_name=cls.last_name2,
        )
        cls.order_item = OrderItem.objects.create(ice=cls.scoop_ice[0], quantity=1)


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

        response = self.client.post(self.url, data={"type": "scoop", "price": 15.5})
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


class OrderListCreateApiViewTest(IceCreamTestAPIData):
    def setUp(self):
        self.url = reverse("orders")

    def test_list_not_logged(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list(self):
        self.client.force_authenticate(user=self.test_user)
        Order.objects.create(worker_owner=self.test_user, status=Order.Status.STARTED)
        response = self.client.get(f"{self.url}?q=tester1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_list_other_user(self):
        self.client.force_authenticate(user=self.test_user2)
        Order.objects.create(worker_owner=self.test_user, status=Order.Status.STARTED)
        response = self.client.get(f"{self.url}?q=tester2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 0)

    def test_create(self):
        self.client.force_authenticate(user=self.test_user)
        order_data = {
            "status": Order.Status.STARTED,
            "order_item": [self.order_item.id],
        }
        response = self.client.post(self.url, data=order_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.data,
            {
                "status": 1,
                "order_item": [self.order_item.id],
                "worker_owner": self.test_user.id,
            },
        )

    def test_create_twice_with_opened_order(self):
        self.client.force_authenticate(user=self.test_user)
        Order.objects.create(worker_owner=self.test_user, status=Order.Status.STARTED)
        order_data = {"status": Order.Status.STARTED, "order_item": []}
        response = self.client.post(self.url, data=order_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(
            "You have already open order, please close it to open new one",
            str(response.data[0]),
        )


class OrderRetrieveUpdateDestroyAPIViewTest(IceCreamTestAPIData):
    def setUp(self):
        self.order = Order.objects.create(
            worker_owner=self.test_user2, status=Order.Status.STARTED
        )
        self.url = reverse("order-manage", kwargs={"id": self.order.id})

    def test_retrieve_not_logged(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve(self):
        self.client.force_authenticate(user=self.test_user2)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.data.pop("time_sell")
        self.assertEqual(
            response.data,
            {
                "id": self.order.id,
                "order_item": [],
                "status": Order.Status.STARTED,
                "worker_owner": self.test_user2.id,
            },
        )

    def test_retrieve_different_user(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_update(self):
        self.client.force_authenticate(user=self.test_user2)
        response = self.client.put(
            self.url,
            data={
                "order_item": [self.order_item.id],
                "status": Order.Status.WAITING,
                "worker_owner": self.test_user2,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "status": Order.Status.WAITING,
                "order_item": [self.order_item.id],
                "worker_owner": self.test_user2.id,
            },
        )

    def test_delete_different_creator(self):
        self.client.force_authenticate(user=self.test_user)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete(self):
        self.client.force_authenticate(user=self.test_user2)
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
