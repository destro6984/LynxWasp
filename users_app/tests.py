from django.contrib.auth import get_user_model
from django.forms import model_to_dict
from django.test import RequestFactory, TestCase
from django.urls import reverse

from users_app.forms import UpdateProfileUser, UpdateUser
from users_app.models import ProfileUser
from users_app.views import ProfileUserUpdate


class RegistrationTest(TestCase):
    username = "tester1"
    email = "tester1@mail.com"
    password = "testing1234"

    def setUp(self):
        url = reverse("register")
        self.response = self.client.get(url)

    def test_register_view_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, "users_app/register.html")
        self.assertContains(self.response, "Join Today")
        self.assertNotContains(self.response, "Lorem Ipsum")

    def test_register_view_form(self):
        response = self.client.post(
            reverse("register"),
            data={
                "username": self.username,
                "email": self.email,
                "password1": self.password,
                "password2": self.password,
                "first_name": "Tom",
                "last_name": "Marvollo",
            },
        )

        self.assertEqual(response.status_code, 302)

        users = get_user_model().objects.all()
        self.assertEqual(users.count(), 1)


class UserProfileTest(TestCase):
    username = "tester1"
    email = "tester1@mail.com"
    password = "testing1234"
    last_name = "Mytnik"
    first_name = "Tomas"

    def setUp(self):
        self.factory = RequestFactory()
        self.test_user = get_user_model().objects.create_user(
            username=self.username,
            email=self.email,
            password=self.password,
            first_name=self.first_name,
            last_name=self.last_name,
        )

    def test_profile_view_created(self):
        user = get_user_model().objects.get(username=self.username)
        self.assertIsInstance(user.profileuser, ProfileUser)

    def test_profile_view_form_update(self):
        self.client.force_login(self.test_user)
        response = self.client.get(reverse("profile"))
        form1 = response.context.get("user_update_form")
        form2 = response.context.get("profile_user_update_form")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(form1, UpdateUser)
        self.assertIsInstance(form2, UpdateProfileUser)

    def test_profile_view_update(self):
        self.client.force_login(self.test_user)
        user_data = model_to_dict(
            self.test_user, fields=["first_name", "last_name", "email"]
        )
        profile_user_data = model_to_dict(self.test_user.profileuser)
        profile_user_data["birth_date"] = "1999-05-14"

        request = self.factory.post(
            reverse("profile"), data={**user_data, **profile_user_data}
        )
        request.user = self.test_user
        response = ProfileUserUpdate.as_view()(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            self.test_user.profileuser.birth_date.strftime("%Y-%m-%d"), "1999-05-14"
        )
