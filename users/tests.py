from django.test import TestCase
from django.urls import reverse
from users.models import CustomUser
from django.contrib.auth import get_user

class RegistrationTestCase(TestCase):
    def test_user_account_is_created(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "user1",
                "first_name": "user1",
                "last_name": "user1",
                "email": "user1@gmail.com",
                "password": "user1"
            }
        )

        user = CustomUser.objects.get(username="user1")

        self.assertEqual(user.first_name, "user1")
        self.assertEqual(user.last_name, "user1")
        self.assertEqual(user.email, "user1@gmail.com")
        self.assertNotEqual(user.password, "user1")
        self.assertTrue(user.check_password("user1"))
    def test_required_fields(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "first_name": "user2",
                "email": "user2@gmail.com"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "username", "This field is required.")
        self.assertFormError(response, "form", "password", "This field is required.")
    
    def test_invalid_email(self):
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "user1",
                "first_name": "user1",
                "last_name": "user1",
                "email": "user1gmail.com",
                "password": "user1"
            }
        )

        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 0)
        self.assertFormError(response, "form", "email", "Enter a valid email address.")
    
    def test_unique_username(self):
        self.client.post(
            reverse("users:register"),
            data={
                "username": "user1",
                "first_name": "user1",
                "last_name": "user1",
                "email": "user1@gmail.com",
                "password": "user1"
            }
        )
        response = self.client.post(
            reverse("users:register"),
            data={
                "username": "user1",
                "first_name": "user1",
                "last_name": "user1",
                "email": "user1@gmail.com",
                "password": "user1"
            }
        )
        user_count = CustomUser.objects.count()

        self.assertEqual(user_count, 1)
        self.assertFormError(response, "form", "username", "A user with that username already exists.")
class LoginTestCase(TestCase):
    def setUp(self):
        #Principes DRY Dont Repeat Yourself
        db_user = CustomUser.objects.create(username = "testuser", first_name = "testuser")
        db_user.set_password("somepassword")
        db_user.save()
    def test_successful_login(self):

        self.client.post(
            reverse("users:login"),
            data={
                "username": "testuser",
                "password": "somepassword"
            }
        )

        user = get_user(self.client)

        self.assertTrue(user.is_authenticated)
    
    def test_wrong_credentials(self):

        self.client.post(
            reverse("users:login"),
            data={
                "username": "wrong_username",
                "password": "somepassword"
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

        self.client.post(
            reverse("users:login"),
            data={
                "username": "testuser",
                "password": "wrongpassword"
            }
        )

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)

    def test_logout(self):

        self.client.login(username="testuser", password="somepassword")

        self.client.get(reverse("users:logout"))

        user = get_user(self.client)

        self.assertFalse(user.is_authenticated)


class ProfileTestCase(TestCase):
    def test_login_required(self):
        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("users:login") + "?next=/users/profile")
    def test_profile_details(self):
        user = CustomUser.objects.create(
            username = "user1", first_name = "user1", last_name = "user1", email = "user1@bk.ru" 
        )
        user.set_password("somepass")
        user.save()

        self.client.login(username = "user1", password = "somepass")

        response = self.client.get(reverse("users:profile"))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, user.username)
        self.assertContains(response, user.first_name)
        self.assertContains(response, user.last_name)
        self.assertContains(response, user.email)
    def test_update_profil(self):
        user = CustomUser.objects.create(
            username = "user1", first_name = "user1", last_name = "user1", email = "user1@bk.ru" 
        )
        user.set_password("somepass")
        user.save()

        self.client.login(username="user1", password="somepass")

        response = self.client.post(
            reverse("users:profile-edit"),
            data={
                "username": "user2",
                "first_name": "user2",
                "last_name": "user2",
                "email": "user2@bk.ru"
            }
        )

        user.refresh_from_db()

        self.assertEqual(user.last_name, "user2")
        self.assertEqual(user.email, "user2@bk.ru")
        self.assertEqual(response.url, reverse("users:profile"))