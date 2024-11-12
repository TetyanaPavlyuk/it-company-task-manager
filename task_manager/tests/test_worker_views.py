from django.contrib.auth import get_user_model
from django.db.models import Q
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position


class PublicWorkerTest(TestCase):
    def setUp(self):
        self.worker = get_user_model().objects.create_user(
            username="Test Worker",
            password="TestPassword123",
        )
        self.worker.save()

        self.url_list = [
            reverse("task_manager:worker-list"),
            reverse(
                "task_manager:worker-detail",
                kwargs={"pk": self.worker.id}
            ),
            reverse("task_manager:worker-create"),
            reverse(
                "task_manager:worker-update",
                kwargs={"pk": self.worker.id}
            ),
            reverse(
                "task_manager:worker-delete",
                kwargs={"pk": self.worker.id}
            )
        ]

    def test_login_required(self):
        response_list = [self.client.get(url) for url in self.url_list]
        for res in response_list:
            self.assertNotEqual(res.status_code, 200)


class PrivateWorkerTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Test Position",
        )
        self.worker1 = get_user_model().objects.create_user(
            username="TestWorker",
            first_name="Test FirstName",
            last_name="Test LastName",
            password="TestPassword123",
            position=self.position,
        )
        self.worker1.save()

        self.worker2 = get_user_model().objects.create_user(
            username="OtherWorker",
            password="TestPassword456",
            position=self.position,
        )
        self.worker2.save()

        self.client.force_login(self.worker1)

        self.url_list = [
            reverse("task_manager:worker-list"),
            reverse(
                "task_manager:worker-detail",
                kwargs={"pk": self.worker1.id}
            ),
            reverse("task_manager:worker-create"),
            reverse(
                "task_manager:worker-update",
                kwargs={"pk": self.worker1.id}
            ),
            reverse(
                "task_manager:worker-delete",
                kwargs={"pk": self.worker1.id}
            )
        ]

        self.response_list = [self.client.get(url) for url in self.url_list]

        self.templates_list = [
            "task_manager/worker_list.html",
            "task_manager/worker_detail.html",
            "task_manager/worker_form.html",
            "task_manager/worker_form.html",
            "task_manager/worker_confirm_delete.html"
        ]

        self.worker_list_url = reverse("task_manager:worker-list")
        self.worker_list_response = self.client.get(self.worker_list_url)

    def test_user_logged_in_required(self):
        for res in self.response_list:
            self.assertEqual(res.status_code, 200)

    def test_display_all_workers(self):
        workers = get_user_model().objects.all()
        self.assertEqual(
            list(self.worker_list_response.context["worker_list"]),
            list(workers)
        )

    def test_search_workers(self):
        search_worker = get_user_model().objects.filter(
            Q(username__icontains="Test") |
            Q(first_name__icontains="Test") |
            Q(last_name__icontains="Test") |
            Q(position__name__icontains="Test")
        )
        search_worker_response = self.client.get(
            self.worker_list_url + "?model=Test"
        )
        self.assertEqual(
            list(search_worker),
            list(search_worker_response.context["worker_list"])
        )

    def test_correct_templates(self):
        for num in range(len(self.templates_list)):
            self.assertTemplateUsed(
                self.response_list[num],
                self.templates_list[num]
            )
