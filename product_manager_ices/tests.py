from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse

from product_manager_ices.forms import AddFlavourForm, AddIceForm, AddOrderItem
from product_manager_ices.models import Flavour, Ices, Order
from users_app.models import User


class IceCreamTestData(TestCase):
    username = "tester1"
    email = "tester1@mail.com"
    password = "testing1234"
    last_name = "Mytnik"
    first_name = "Tomas"

    @classmethod
    def setUpTestData(cls):
        cls.admin_user = User.objects.create_superuser(
            username="admin", email="admin@example.com", password="test"
        )
        cls.test_user = get_user_model().objects.create_user(
            username=cls.username,
            email=cls.email,
            password=cls.password,
            first_name=cls.first_name,
            last_name=cls.last_name,
        )
        cls.thai_ice = Ices.objects.create(type="thai", price=10)
        cls.scoope_ice = Ices.objects.create(type="scoope", price=5)
        cls.chocolate = Flavour.objects.create(flavour="chocolate")
        cls.cream = Flavour.objects.create(flavour="cream")
        cls.strawberry = Flavour.objects.create(flavour="strawberry")

    def setUp(self):
        self.factory = RequestFactory()


class IceViewTest(IceCreamTestData):
    def test_ice_view_template(self):
        self.client.force_login(self.admin_user)
        response = self.client.get(reverse("add-ice"))
        form1 = response.context.get("form_type")
        form2 = response.context.get("form_flavour")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form1, AddIceForm)
        self.assertIsInstance(form2, AddFlavourForm)

    def test_ice_view_not_super_user(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse("add-ice"))
        self.assertContains(response, "Log in as admin to add new ices")

    def test_ice_view_add_ice_type(self):
        self.client.force_login(self.admin_user)

        ice_data = {"type": "Mixed", "price": "45"}

        response = self.client.post(reverse("add-ice"), data={**ice_data}, follow=True)

        self.assertContains(response, "Type Added")

    def test_ice_view_add_ice_type_wrong_input(self):
        self.client.force_login(self.admin_user)

        ice_data = {"price": "45"}

        response = self.client.post(reverse("add-ice"), data={**ice_data}, follow=True)

        self.assertNotContains(response, "Type Added")

    def test_ice_view_add_ice_flavour(self):
        self.client.force_login(self.admin_user)

        ice_data = {"flavour": "Mixed"}

        response = self.client.post(reverse("add-ice"), data={**ice_data}, follow=True)

        self.assertContains(response, "Flavour Added")

    def test_ice_view_add_ice_flavour_wrong_input(self):
        self.client.force_login(self.admin_user)

        ice_data = {"flavour": ""}

        response = self.client.post(reverse("add-ice"), data={**ice_data}, follow=True)

        self.assertNotContains(response, "Flavour Added")

    def test_ice_view_add_ice_type_flavour_only_correct_added(self):
        self.client.force_login(self.admin_user)

        mixed_ice_data = {"flavour": "Mixed", "type": "Mixed", "price": "45"}

        response = self.client.post(
            reverse("add-ice"), data={**mixed_ice_data}, follow=True
        )

        self.assertContains(response, "Type Added")


class OrderItemViewTest(IceCreamTestData):
    def test_create_order_item_view_not_logged(self):
        response = self.client.get(reverse("create-order-item"))
        self.assertRedirects(response, "/user/login/?next=/order-items/")

    def test_create_order_item_view_template_no_opened_order(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse("create-order-item"))
        form = response.context.get("add_order_form")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form, AddOrderItem)
        self.assertFalse(
            Order.objects.filter(worker_owner=self.test_user, status=1).count(), 1
        )
        self.assertContains(response, "Open Order")

    def test_create_order_item_view_template_opened_order(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse("create-order-item"))
        self.client.post(reverse("open-order"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Order.objects.filter(worker_owner=self.test_user, status=1).count(), 1
        )

    def test_create_order_item_view_add(self):
        self.client.force_login(self.test_user),
        self.client.post(reverse("open-order"))

        order_item_data = {
            "ice": self.scoope_ice,
            "quantity": 1,
            "flavour": [self.chocolate, self.cream, self.strawberry],
        }
        response = self.client.post(
            reverse("create-order-item"), data=order_item_data, follow=True
        )
        self.assertEqual(len(self.test_user.order_set.all()), 1)
        self.assertEqual(response.status_code, 200)


class OrderTest(IceCreamTestData):
    def test_open_order(self):
        self.client.force_login(self.test_user)
        self.client.post(reverse("open-order"), follow=True)
        self.assertEqual(
            Order.objects.filter(worker_owner=self.test_user, status=1).count(), 1
        )

    def test_open_order_twice_wrong(self):
        self.client.force_login(self.test_user)
        response = self.client.post(reverse("open-order"))  # noqa
        response2 = self.client.post(reverse("open-order"), follow=True)
        self.assertContains(response2, "You have already opened order")
