from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import TaskType


class PublicTaskTypeTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(
            name="Test Task Type",
        )
        self.task_type.save()

        self.urls_list = [
            reverse("task_manager:task-type-list"),
            reverse("task_manager:task-type-create"),
            reverse(
                "task_manager:task-type-update",
                kwargs={"pk": self.task_type.id}
            ),
            reverse(
                "task_manager:task-type-delete",
                kwargs={"pk": self.task_type.id}
            ),
        ]

    def test_login_required(self):
        response_list = [self.client.get(url) for url in self.urls_list]
        for res in response_list:
            self.assertNotEqual(res.status_code, 200)


class PrivateTaskTypeTest(TestCase):
    def setUp(self):
        self.task_type1 = TaskType.objects.create(
            name="Test Task Type",
        )
        self.task_type1.save()

        self.worker = get_user_model().objects.create_user(
            username="TestWorker",
            password="TestPassword123",
        )
        self.worker.save()

        self.client.force_login(self.worker)

        self.task_type2 = TaskType.objects.create(
            name="Other Task Type",
        )
        self.task_type2.save()

        self.urls_list = [
            reverse("task_manager:task-type-list"),
            reverse("task_manager:task-type-create"),
            reverse(
                "task_manager:task-type-update",
                kwargs={"pk": self.task_type1.id}
            ),
            reverse(
                "task_manager:task-type-delete",
                kwargs={"pk": self.task_type1.id}
            ),
        ]

        self.response_list = [self.client.get(url) for url in self.urls_list]

        self.templates_list = [
            "task_manager/tasktype_list.html",
            "task_manager/tasktype_form.html",
            "task_manager/tasktype_form.html",
            "task_manager/tasktype_confirm_delete.html",
        ]

        self.task_type_list_url = reverse("task_manager:task-type-list")
        self.task_type_list_response = self.client.get(
            self.task_type_list_url
        )

    def test_user_logged_in_required(self):
        for res in self.response_list:
            self.assertEqual(res.status_code, 200)

    def test_display_all_task_types(self):
        task_types = TaskType.objects.all()
        self.assertEqual(
            list(self.task_type_list_response.context["task_type_list"]),
            list(task_types)
        )

    def test_search_task_types(self):
        search_task_type = TaskType.objects.filter(
            name__icontains="Test"
        )
        search_task_type_response = self.client.get(
            self.task_type_list_url + "?model=Test"
        )
        self.assertEqual(
            list(search_task_type),
            list(search_task_type_response.context["task_type_list"])
        )

    def test_correct_templates(self):
        for num in range(len(self.templates_list)):
            self.assertTemplateUsed(
                self.response_list[num],
                self.templates_list[num]
            )
