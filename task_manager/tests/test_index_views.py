from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import (
    Position,
    TaskType,
    Task,
    New,
)


class PublicIndexTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Test Position",
        )
        self.position.save()

        self.worker = get_user_model().objects.create_user(
            username="TestWorker",
            password="TestPassword123",
            position=self.position,
        )
        self.worker.save()

        self.task_type = TaskType.objects.create(
            name="Test Task Type"
        )
        self.task_type.save()

        self.task = Task.objects.create(
            name="Test Task",
            deadline="2024-06-14",
            task_type=self.task_type,
        )
        self.task.save()
        self.task.assignees.add(self.worker)

        self.url = reverse("task_manager:index")

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertNotEqual(response.status_code, 200)


class PrivateIndexTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Test Position",
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

        self.task_type = TaskType.objects.create(
            name="Test Task Type"
        )
        self.task_type.save()

        self.task = Task.objects.create(
            name="Test Task",
            deadline="2024-06-14",
            task_type=self.task_type,
        )
        self.task.save()
        self.task.assignees.add(self.worker)

        self.client.force_login(self.worker)

        self.url = reverse("task_manager:index")

    def test_retrieve_user_index(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

        worker_count = get_user_model().objects.count()
        completed_tasks_count = Task.objects.filter(
            is_completed="True"
        ).count()
        defined_tasks_count = Task.objects.filter(
            is_completed="False"
        ).count()
        news = New.objects.all()
        self.assertEqual(response.context["num_experts"], worker_count)
        self.assertEqual(
            response.context["num_completed_tasks"], completed_tasks_count
        )
        self.assertEqual(
            response.context["num_defined_tasks"], defined_tasks_count
        )
        self.assertEqual(list(response.context["new_list"]), list(news))
