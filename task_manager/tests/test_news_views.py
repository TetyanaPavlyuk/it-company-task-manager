from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import New, Position


class PublicNewsTest(TestCase):
    def setUp(self):
        self.worker = get_user_model().objects.create_user(
            username="Test Worker",
            password="TestPassword123",
        )
        self.news = New.objects.create(
            name="Test News",
            description="Some Text",
            author=self.worker,
        )
        self.news.save()

        self.urls_list = [
            reverse("task_manager:new-create"),
            reverse(
                "task_manager:new-update",
                kwargs={"pk": self.news.id}
            ),
            reverse(
                "task_manager:new-delete",
                kwargs={"pk": self.news.id}
            ),
        ]

    def test_login_required(self):
        response_list = [self.client.get(url) for url in self.urls_list]
        for res in response_list:
            self.assertNotEqual(res.status_code, 200)

    def test_no_author_update_news(self):
        no_author = get_user_model().objects.create_user(
            username="NoAuthor",
            password="TestPassword456",
        )
        no_author.save()
        self.client.force_login(no_author)
        response = self.client.get(self.urls_list[1])
        self.assertNotEqual(response.status_code, 200)


class PrivateNewsTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Test Position"
        )
        self.position.save()

        self.worker = get_user_model().objects.create_user(
            username="TestWorker",
            first_name="Test FirstName",
            last_name="Test LastName",
            password="TestPassword123",
            position=self.position,
        )
        self.worker.save()

        self.news = New.objects.create(
            name="Test News",
            description="Some Text",
            author=self.worker,
        )

        self.client.force_login(self.worker)

        self.urls_list = [
            reverse("task_manager:new-create"),
            reverse(
                "task_manager:new-update",
                kwargs={"pk": self.news.id}
            ),
            reverse(
                "task_manager:new-delete",
                kwargs={"pk": self.news.id}
            ),
        ]

        self.response_list = [self.client.get(url) for url in self.urls_list]

        self.templates_list = [
            "task_manager/new_form.html",
            "task_manager/new_form.html",
            "task_manager/new_confirm_delete.html",
        ]

    def test_user_logged_in_required(self):
        for res in self.response_list:
            self.assertEqual(res.status_code, 200)

    def test_correct_templates(self):
        for num in range(len(self.templates_list)):
            self.assertTemplateUsed(
                self.response_list[num],
                self.templates_list[num]
            )
