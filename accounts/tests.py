from django.test import TestCase
from django.urls import reverse
from .models import User
from .forms import AccountsForm


class TestSignUpView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        response = self.client.get(reverse("accounts:signup"))
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        test_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, test_data)
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )

        self.assertTrue(
            User.objects.filter(
                username=test_data["username"],
                email=test_data["email"],
            ).exists()
        )

    def test_failure_post_with_empty_form(self):
        empty_data = {
            "username": "",
            "email": "",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, empty_data)
        self.assertEqual(response.status_code, 200)

        self.assertEqual(User.objects.count(), 0)

        form = AccountsForm(data=empty_data)

        self.assertEqual(form.errors["username"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["email"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["password1"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["password2"], ["このフィールドは必須です。"])

    def test_failure_post_with_empty_username(self):
        empty_data = {
            "username": "",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, empty_data)
        self.assertEqual(response.status_code, 200)

        form = AccountsForm(data=empty_data)

        self.assertEqual(form.errors["username"], ["このフィールドは必須です。"])

        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_empty_email(self):
        empty_data = {
            "username": "testuser",
            "email": "",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        response = self.client.post(self.url, empty_data)
        self.assertEqual(response.status_code, 200)

        form = AccountsForm(data=empty_data)

        self.assertEqual(form.errors["email"], ["このフィールドは必須です。"])

        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_empty_password(self):
        empty_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "",
            "password2": "",
        }

        response = self.client.post(self.url, empty_data)
        self.assertEqual(response.status_code, 200)

        form = AccountsForm(data=empty_data)

        self.assertEqual(form.errors["password1"], ["このフィールドは必須です。"])
        self.assertEqual(form.errors["password2"], ["このフィールドは必須です。"])

        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_duplicated_user(self):
        duplicated_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }

        User.objects.create(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )

        response = self.client.post(self.url, duplicated_data)
        self.assertEqual(response.status_code, 200)

        form = AccountsForm(data=duplicated_data)
        self.assertEqual(form.errors["username"], ["同じユーザー名が既に登録済みです。"])
        self.assertEqual(form.errors["email"], ["この Email を持った ユーザー が既に存在します。"])

        self.assertEqual(User.objects.count(), 1)

    def test_failure_post_with_invalid_email(self):
        pass

    def test_failure_post_with_too_short_password(self):
        pass

    def test_failure_post_with_password_similar_to_username(self):
        pass

    def test_failure_post_with_only_numbers_password(self):
        pass

    def test_failure_post_with_mismatch_password(self):
        pass


class TestLoginView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_empty_password(self):
        pass


class TestLogoutView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileView(TestCase):
    def test_success_get(self):
        pass


class TestUserProfileEditView(TestCase):
    def test_success_get(self):
        pass

    def test_success_post(self):
        pass

    def test_failure_post_with_not_exists_user(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_user(self):
        pass

    def test_failure_post_with_self(self):
        pass


class TestUnfollowView(TestCase):
    def test_success_post(self):
        pass

    def test_failure_post_with_not_exist_tweet(self):
        pass

    def test_failure_post_with_incorrect_user(self):
        pass


class TestFollowingListView(TestCase):
    def test_success_get(self):
        pass


class TestFollowerListView(TestCase):
    def test_success_get(self):
        pass
