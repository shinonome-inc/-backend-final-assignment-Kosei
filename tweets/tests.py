from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from tweets.forms import TweetForm
from tweets.models import Tweet, Favorite


class TestHomeView(TestCase):
    def test_success_get(self):
        self.user = User.objects.create(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )
        self.client.force_login(self.user)
        Tweet.objects.create(author=self.user, text="test tweet")
        response = self.client.get(reverse("tweets:home"))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context["object_list"], Tweet.objects.all())


class TestTweetCreateView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )
        self.url = reverse("tweets:create")
        self.client.force_login(self.user)

    def test_success_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_success_post(self):
        test_data = {"text": "test tweet"}
        response = self.client.post(self.url, test_data)
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
        self.assertTrue(Tweet.objects.filter(text=test_data["text"]).exists())

    def test_failure_post_with_empty_content(self):
        test_data = {"text": ""}
        response = self.client.post(self.url, test_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tweet.objects.filter(text=test_data["text"]).exists())
        form = TweetForm(data=test_data)
        self.assertEqual(form.errors["text"], ["このフィールドは必須です。"])

    def test_failure_post_with_too_long_content(self):
        test_data = {"text": "a" * 257}
        response = self.client.post(self.url, test_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Tweet.objects.filter(text=test_data["text"]).exists())
        form = TweetForm(data=test_data)
        self.assertEqual(
            form.errors["text"], ["この値は 256 文字以下でなければなりません( 257 文字になっています)。"]
        )


class TestTweetDetailView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )
        self.client.force_login(self.user)
        self.data = Tweet.objects.create(author=self.user, text="test tweet")

    def test_success_get(self):
        response = self.client.get(
            reverse("tweets:detail", kwargs={"pk": self.data.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["object"], self.data)


class TestTweetDeleteView(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(
            username="testuser1",
            email="test1@example.com",
            password="testpassword1",
        )
        self.user2 = User.objects.create_user(
            username="testuser2",
            email="test2@example.com",
            password="testpassword2",
        )

        self.data = Tweet.objects.create(author=self.user1, text="test tweet")
        self.url = reverse("tweets:delete", kwargs={"pk": self.data.pk})

    def test_success_post(self):
        self.client.force_login(self.user1)
        response = self.client.post(self.url)
        self.assertRedirects(
            response,
            reverse("tweets:home"),
            status_code=302,
            target_status_code=200,
            msg_prefix="",
            fetch_redirect_response=True,
        )
        self.assertFalse(Tweet.objects.filter(text="test tweet").exists())

    def test_failure_post_with_not_exist_tweet(self):
        self.client.force_login(self.user1)
        response = self.client.post(reverse("tweets:delete", kwargs={"pk": 714}))
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Tweet.objects.count(), 1)

    def test_failure_post_with_incorrect_user(self):
        self.client.force_login(self.user2)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Tweet.objects.count(), 1)


class TestFavoriteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )
        self.client.force_login(self.user)
        self.data = Tweet.objects.create(author=self.user, text="test tweet")
        self.url = reverse("tweets:like", kwargs={"pk": self.data.pk})

    def test_success_post(self):
        response = self.client.post(self.url)
        # self.assertEqual(response.status_code, 200)
        self.assertTrue(Favorite.objects.filter(tweet=self.data, user=self.user))

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(reverse("tweets:like", kwargs={"pk": 714}))
        self.assertContains(response, "Not Found", status_code=404)
        self.assertEqual(Favorite.objects.all().count(), 0)

    def test_failure_post_with_favorited_tweet(self):
        Favorite.objects.create(tweet=self.data, user=self.user)
        response = self.client.post(self.url)
        # self.assertEqual(response.status_code,200)
        self.assertEqual(Favorite.objects.all().count(), 1)


class TestUnfavoriteView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword",
        )
        self.client.force_login(self.user)
        self.data = Tweet.objects.create(author=self.user, text="test tweet")
        Favorite.objects.create(tweet=self.data, user=self.user)
        self.url = reverse("tweets:unlike", kwargs={"pk": self.data.pk})

    def test_success_post(self):
        response = self.client.post(self.url)
        # self.assertEqual(response.status_code, 200)
        self.assertEqual(Favorite.objects.all().count(), 0)

    def test_failure_post_with_not_exist_tweet(self):
        response = self.client.post(reverse("tweets:unlike", kwargs={"pk": 714}))
        self.assertContains(response, "Not Found", status_code=404)
        self.assertEqual(Favorite.objects.all().count(), 1)

    def test_failure_post_with_unfavorited_tweet(self):
        Favorite.objects.filter(tweet=self.data, user=self.user).delete()
        response = self.client.post(self.url)
        # self.assertEqual(response.status_code, 200)
