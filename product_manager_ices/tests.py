from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse

from product_manager_ices.forms import AddFlavourForm, AddIceForm, AddOrderItem
from product_manager_ices.models import Flavour, Ices, Order, OrderItem
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
        cls.blueberry = Flavour.objects.create(flavour="blueberry")

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
            Order.objects.filter(
                worker_owner=self.test_user, status=Order.Status.STARTED
            ).count(),
            1,
        )
        self.assertContains(response, "Open Order")

    def test_create_order_item_view_template_opened_order(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse("create-order-item"))
        self.client.post(reverse("open-order"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            Order.objects.filter(
                worker_owner=self.test_user, status=Order.Status.STARTED
            ).count(),
            1,
        )

    def test_create_order_item_view_add_scoope(self):
        self.client.force_login(self.test_user),
        Order.objects.create(worker_owner=self.test_user, status=Order.Status.STARTED)

        order_item_data = {
            "ice": self.scoope_ice.id,
            "quantity": 1,
            "flavour": [self.chocolate.id],
        }
        response = self.client.post(
            reverse("create-order-item"), data=order_item_data, follow=True
        )
        self.assertEqual(len(self.test_user.order_set.all()), 1)
        self.assertContains(response, "Added to cart")

    def test_create_order_item_view_add_scoope_more_flavour_than_quantity(self):
        self.client.force_login(self.test_user),
        Order.objects.create(worker_owner=self.test_user, status=Order.Status.STARTED)

        order_item_data = {
            "ice": self.scoope_ice.id,
            "quantity": 1,
            "flavour": [self.chocolate.id, self.strawberry.id],
        }
        response = self.client.post(
            reverse("create-order-item"), data=order_item_data, follow=True
        )
        self.assertContains(response, "Only One flavour per scoope")

    def test_create_order_item_view_add_more_than_three_thai(self):
        self.client.force_login(self.test_user),
        Order.objects.create(worker_owner=self.test_user, status=Order.Status.STARTED)

        order_item_data = {
            "ice": self.thai_ice.id,
            "quantity": 1,
            "flavour": [
                self.chocolate.id,
                self.cream.id,
                self.strawberry.id,
                self.blueberry.id,
            ],
        }
        response = self.client.post(
            reverse("create-order-item"), data=order_item_data, follow=True
        )
        self.assertEqual(len(self.test_user.order_set.all()), 1)
        self.assertContains(
            response, "Thai Ice cannot be mixed with more than 3 flavours"
        )

    def test_delete_order_item_view(self):
        self.client.force_login(self.test_user),
        opened_order = Order.objects.create(
            worker_owner=self.test_user, status=Order.Status.STARTED
        )

        order_item = OrderItem.objects.create(ice=self.scoope_ice, quantity=1)
        order_item.flavour.set([self.chocolate])
        order_item.order.set([opened_order])

        self.client.post(reverse("delete-order-item", kwargs={"pk": order_item.id}))
        self.assertFalse(len(OrderItem.objects.all()))


class OrderTest(IceCreamTestData):
    def test_list_order(self):
        self.client.force_login(self.test_user)
        Order.objects.create(worker_owner=self.test_user, status=Order.Status.STARTED)
        response = self.client.get(reverse("list-order"), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_open_order(self):
        self.client.force_login(self.test_user)
        self.client.post(reverse("open-order"), follow=True)
        self.assertEqual(
            Order.objects.filter(
                worker_owner=self.test_user, status=Order.Status.STARTED
            ).count(),
            1,
        )

    def test_open_order_twice_wrong(self):
        self.client.force_login(self.test_user)
        response = self.client.post(reverse("open-order"))  # noqa
        response2 = self.client.post(reverse("open-order"), follow=True)
        self.assertContains(response2, "You have already opened order")

    def test_postpone_order(self):
        self.client.force_login(self.test_user)
        opened_order = Order.objects.create(
            worker_owner=self.test_user, status=Order.Status.STARTED
        )
        self.client.post(reverse("postpone-order", kwargs={"pk": opened_order.id}))
        opened_order.refresh_from_db()
        self.assertNotEqual(len(Order.objects.all()), 0)
        self.assertEqual(Order.objects.filter(worker_owner=self.test_user).count(), 1)
        self.assertNotEqual(opened_order.status, 1)

    def test_reactivate_order(self):
        self.client.force_login(self.test_user)
        opened_order = Order.objects.create(
            worker_owner=self.test_user, status=Order.Status.STARTED
        )
        self.client.post(
            reverse("reactivate-order", kwargs={"pk": opened_order.id}), follow=True
        )
        opened_order.refresh_from_db()
        self.assertNotEqual(opened_order.status, 3)

    def test_delete_order(self):
        self.client.force_login(self.test_user)
        opened_order = Order.objects.create(
            worker_owner=self.test_user, status=Order.Status.STARTED
        )
        self.client.post(reverse("delete-order", kwargs={"pk": opened_order.id}))

        self.assertNotEqual(len(Order.objects.all()), 1)
        self.assertEqual(Order.objects.filter(worker_owner=self.test_user).count(), 0)
