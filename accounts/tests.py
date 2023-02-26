from django.contrib.auth import SESSION_KEY
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from mysite.settings import LOGIN_REDIRECT_URL, LOGOUT_REDIRECT_URL
from tweets.models import Tweet

from .forms import AccountsForm, LoginForm
from .models import Friendship, User


class TestSignUpSuccessView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        test_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, test_data)
        self.assertRedirects(
            response,
            reverse(LOGIN_REDIRECT_URL),
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


class TestSignUpFailureView(TestCase):
    def setUp(self):
        self.url = reverse("accounts:signup")

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
        email_failure_data = {
            "username": "testuser",
            "email": "test_email",
            "password1": "testpassword",
            "password2": "testpassword",
        }
        response = self.client.post(self.url, email_failure_data)
        self.assertEqual(response.status_code, 200)
        form = AccountsForm(data=email_failure_data)
        self.assertEqual(form.errors["email"], ["有効なメールアドレスを入力してください。"])
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_too_short_password(self):
        password_failure_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "short",
            "password2": "short",
        }
        response = self.client.post(self.url, password_failure_data)
        self.assertEqual(response.status_code, 200)
        form = AccountsForm(data=password_failure_data)
        self.assertEqual(form.errors["password2"], ["このパスワードは短すぎます。最低 8 文字以上必要です。"])
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_password_similar_to_username(self):
        password_failure_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testuser",
            "password2": "testuser",
        }
        response = self.client.post(self.url, password_failure_data)
        self.assertEqual(response.status_code, 200)
        form = AccountsForm(data=password_failure_data)
        self.assertEqual(form.errors["password2"], ["このパスワードは ユーザー名 と似すぎています。"])
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_only_numbers_password(self):
        password_failure_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "16475843",
            "password2": "16475843",
        }
        response = self.client.post(self.url, password_failure_data)
        self.assertEqual(response.status_code, 200)
        form = AccountsForm(data=password_failure_data)
        self.assertEqual(form.errors["password2"], ["このパスワードは数字しか使われていません。"])
        self.assertEqual(User.objects.count(), 0)

    def test_failure_post_with_mismatch_password(self):
        password_failure_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password1": "testpassword",
            "password2": "testpassword1",
        }
        response = self.client.post(self.url, password_failure_data)
        self.assertEqual(response.status_code, 200)
        form = AccountsForm(data=password_failure_data)
        self.assertEqual(form.errors["password2"], ["確認用パスワードが一致しません。"])
        self.assertEqual(User.objects.count(), 0)


class TestLoginView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )
        self.url = reverse("accounts:login")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        test_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword",
        }
        response = self.client.post(self.url, test_data)
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
        self.assertIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_not_exists_user(self):
        test_data = {
            "username": "no_testuser",
            "password": "testpassword",
        }
        response = self.client.post(self.url, test_data)
        self.assertEqual(response.status_code, 200)
        form = LoginForm(data=test_data)
        self.assertEqual(
            form.errors["__all__"],
            ["正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。"],
        )
        self.assertNotIn(SESSION_KEY, self.client.session)

    def test_failure_post_with_empty_password(self):
        test_data = {
            "username": "testuser",
            "password": "test_password",
        }
        response = self.client.post(self.url, test_data)
        self.assertEqual(response.status_code, 200)
        form = LoginForm(data=test_data)
        self.assertEqual(
            form.errors["__all__"],
            ["正しいユーザー名とパスワードを入力してください。どちらのフィールドも大文字と小文字は区別されます。"],
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestLogoutView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )
        self.url = reverse("accounts:logout")

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            reverse(LOGOUT_REDIRECT_URL),
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
        self.assertNotIn(SESSION_KEY, self.client.session)


class TestUserProfileView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            email="test1@example.com",
            password="testpassword1",
        )
        self.client.force_login(self.user1)
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
            password="testpassword2",
        )
        Friendship.objects.create(followee=self.user2, follower=self.user1)
        Friendship.objects.create(followee=self.user1, follower=self.user2)
        self.client.force_login(self.user1)

    def test_success_get(self):
        self.data = Tweet.objects.create(author=self.user1, text="test tweet")
        self.url = reverse("accounts:user_profile", kwargs={"username": "testuser1"})
        response = self.client.get(self.url)
        self.assertQuerysetEqual(
            response.context["object_list"],
            Tweet.objects.filter(author=self.user1),
        )
        self.assertEqual(response.context["num_follows"], 1)
        self.assertEqual(response.context["num_followers"], 1)


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
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            email="test1@example.com",
            password="testpassword1",
        )
        self.client.force_login(self.user1)

    def test_success_post(self):
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
            password="testpassword2",
        )
        self.url = reverse("accounts:follow", kwargs={"username": self.user2.username})
        response = self.client.post(self.url)
        self.assertTrue(
            Friendship.objects.filter(follower=self.user1, followee=self.user2).exists()
        )
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )

    def test_failure_post_with_not_exist_user(self):
        self.url = reverse("accounts:follow", kwargs={"username": "empty_user"})
        response = self.client.post(self.url)
        self.assertContains(response, "Not Found", status_code=404)
        self.assertEqual(Friendship.objects.count(), 0)

    def test_failure_post_with_self(self):
        self.url = reverse("accounts:follow", kwargs={"username": self.user1.username})
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Friendship.objects.count(), 0)
        self.assertEqual(
            str(list(get_messages(response.wsgi_request))[0]), "自分自身のことはフォローできません。"
        )


class TestUnfollowView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            email="test1@example.com",
            password="testpassword1",
        )
        self.client.force_login(self.user1)
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
            password="testpassword2",
        )
        Friendship.objects.create(followee=self.user2, follower=self.user1)

    def test_success_post(self):
        self.url = reverse(
            "accounts:unfollow", kwargs={"username": self.user2.username}
        )
        response = self.client.post(self.url)
        self.assertFalse(
            Friendship.objects.filter(followee=self.user2, follower=self.user1).exists()
        )
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )

    def test_failure_post_with_not_exist_tweet(self):
        self.url = reverse("accounts:unfollow", kwargs={"username": "empty_user"})
        response = self.client.post(self.url)
        self.assertContains(response, "Not Found", status_code=404)
        self.assertEqual(Friendship.objects.count(), 1)

    def test_failure_post_with_incorrect_user(self):
        self.url = reverse(
            "accounts:unfollow", kwargs={"username": self.user1.username}
        )
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Friendship.objects.count(), 1)
        self.assertEqual(
            str(list(get_messages(response.wsgi_request))[0]), "自分自身のことはアンフォローできません。"
        )


class TestFollowingListView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            email="test1@example.com",
            password="testpassword1",
        )
        self.client.force_login(self.user1)
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
            password="testpassword2",
        )
        Friendship.objects.create(followee=self.user2, follower=self.user1)

    def test_success_get(self):
        self.url = reverse(
            "accounts:following_list", kwargs={"username": self.user1.username}
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)


class TestFollowerListView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            email="test1@example.com",
            password="testpassword1",
        )
        self.client.force_login(self.user1)
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
            password="testpassword2",
        )
        Friendship.objects.create(followee=self.user2, follower=self.user1)

    def test_success_get(self):
        self.url = reverse(
            "accounts:follower_list", kwargs={"username": self.user1.username}
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
