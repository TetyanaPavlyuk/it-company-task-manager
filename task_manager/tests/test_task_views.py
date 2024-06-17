from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Task, TaskType


class PublicTaskTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(
            name="Test Task Type",
        )
        self.task_type.save()

        self.worker = get_user_model().objects.create_user(
            username="Test Worker",
            password="TestPassword123",
        )
        self.worker.save()

        self.task = Task.objects.create(
            name="Test Task",
            description="Some Description",
            deadline="2024-06-14",
            is_completed=True,
            task_type=self.task_type,
        )
        self.task.save()
        self.task.assignees.add(self.worker)

        self.urls_list = [
            reverse("task_manager:task-list"),
            reverse(
                "task_manager:task-detail",
                kwargs={"pk": self.task.id}
            ),
            reverse("task_manager:task-create"),
            reverse(
                "task_manager:task-update",
                kwargs={"pk": self.task.id}
            ),
            reverse(
                "task_manager:task-delete",
                kwargs={"pk": self.task.id}
            )
        ]

    def test_login_required(self):
        response_list = [self.client.get(url) for url in self.urls_list]
        for res in response_list:
            self.assertNotEqual(res.status_code, 200)


class PrivateTaskTest(TestCase):
    def setUp(self):
        self.task_type = TaskType.objects.create(
            name="Test Task Type",
        )
        self.task_type.save()

        self.worker = get_user_model().objects.create_user(
            username="TestWorker",
            first_name="Test FirstName",
            last_name="Test LastName",
            password="TestPassword123",
        )
        self.worker.save()

        self.task1 = Task.objects.create(
            name="Test Task",
            description="Some Description",
            deadline="2024-06-14",
            is_completed=True,
            task_type=self.task_type,
        )
        self.task1.save()
        self.task1.assignees.add(self.worker)

        self.task2 = Task.objects.create(
            name="Other Task",
            deadline="2024-07-07",
        )
        self.task2.save()
        self.task2.assignees.add(self.worker)

        self.client.force_login(self.worker)

        self.urls_list = [
            reverse("task_manager:task-list"),
            reverse(
                "task_manager:task-detail",
                kwargs={"pk": self.task1.id}
            ),
            reverse("task_manager:task-create"),
            reverse(
                "task_manager:task-update",
                kwargs={"pk": self.task1.id}
            ),
            reverse(
                "task_manager:task-delete",
                kwargs={"pk": self.task1.id}
            )
        ]

        self.response_list = [self.client.get(url) for url in self.urls_list]

        self.templates_list = [
            "task_manager/task_list.html",
            "task_manager/task_detail.html",
            "task_manager/task_form.html",
            "task_manager/task_form.html",
            "task_manager/task_confirm_delete.html"
        ]

        self.task_list_url = reverse("task_manager:task-list")
        self.task_list_response = self.client.get(self.task_list_url)

    def test_user_logged_in_required(self):
        for res in self.response_list:
            self.assertEqual(res.status_code, 200)

    def test_display_all_tasks(self):
        tasks = Task.objects.all()
        self.assertEqual(
            list(self.task_list_response.context["task_list"]),
            list(tasks)
        )

    def test_search_task(self):
        search_task = Task.objects.filter(name__icontains="Test")
        search_task_response = self.client.get(
            self.task_list_url + "?model=Test"
        )
        self.assertEqual(
            list(search_task),
            list(search_task_response.context["task_list"])
        )

    def test_correct_templates(self):
        for num in range(len(self.templates_list)):
            self.assertTemplateUsed(
                self.response_list[num],
                self.templates_list[num]
            )
