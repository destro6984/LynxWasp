from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase
from django.urls import reverse

from product_manager_ices.forms import AddFlavourForm, AddIceForm
from users_app.models import User


class IceViewTest(TestCase):
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

    def setUp(self):
        self.factory = RequestFactory()

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
