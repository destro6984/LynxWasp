from django.test import TestCase
from django.urls import reverse


class RegistrationTest(TestCase):
    username = "tester1"
    email = "tester1@mail.com"

    def setUp(self):
        url = reverse("register")
        self.response = self.client.get(url)

    def test_register_view(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "users_app/register.html")
        self.assertContains(self.response, "Join Today")
        self.assertNotContains(self.response, "Lorem Ipsum")
