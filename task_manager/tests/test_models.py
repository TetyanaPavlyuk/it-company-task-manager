import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from task_manager.models import Position, TaskType, Task, New


class ModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.position = Position.objects.create(
            name="Test Position",
        )

        cls.worker = get_user_model().objects.create_user(
            username="TestWorker",
            first_name="Test FirstName",
            last_name="Test LastName",
            password="TestPassword123",
            position=cls.position,
        )

        cls.task_type = TaskType.objects.create(
            name="Test Task Type"
        )

        cls.task = Task.objects.create(
            name="Test Task",
            description="Some Description",
            deadline="2024-06-14",
            is_completed=True,
            task_type=cls.task_type,
        )
        cls.task.assignees.add(cls.worker)

        cls.news = New.objects.create(
            name="Test New",
            description="Some Description",
            author=cls.worker,
        )

    def test_position_str(self):
        position = Position.objects.get(id=1)
        self.assertEqual(str(position), position.name)

    def test_worker_str(self):
        worker = get_user_model().objects.get(id=1)
        self.assertEqual(
            str(worker),
            f"{worker.position}: {worker.last_name} {worker.first_name}"
        )

    def test_worker_get_absolute_url(self):
        worker = get_user_model().objects.get(id=1)
        self.assertEqual(
            worker.get_absolute_url(),
            f"/workers/{worker.id}/detail/"
        )

    def test_create_worker(self):
        worker = get_user_model().objects.get(id=1)
        position = Position.objects.get(id=1)
        self.assertEqual(worker.username, "TestWorker")
        self.assertEqual(worker.first_name, "Test FirstName")
        self.assertEqual(worker.last_name, "Test LastName")
        self.assertTrue(worker.check_password("TestPassword123"))
        self.assertEqual(worker.position, position)

    def test_task_type_str(self):
        task_type = TaskType.objects.get(id=1)
        self.assertEqual(str(task_type), task_type.name)

    def test_task_str(self):
        task = Task.objects.get(id=1)
        self.assertEqual(
            str(task),
            f"{task.name} ({task.priority}) / {task.deadline}"
        )

    def test_task_get_absolute_url(self):
        task = Task.objects.get(id=1)
        self.assertEqual(
            task.get_absolute_url(),
            f"/tasks/{task.id}/detail/"
        )

    def test_create_task(self):
        task = Task.objects.get(id=1)
        task_type = TaskType.objects.get(id=1)
        assignees = (get_user_model().objects.
                     prefetch_related("tasks").filter(tasks=task))
        self.assertEqual(task.name, "Test Task")
        self.assertEqual(task.description, "Some Description")
        self.assertEqual(task.deadline, datetime.date(2024, 6, 14))
        self.assertTrue(task.is_completed),
        self.assertEqual(task.priority, "U")
        self.assertEqual(task.task_type, task_type)
        self.assertEqual(list(task.assignees.all()), list(assignees))

    def test_news_str(self):
        news = New.objects.get(id=1)
        self.assertEqual(str(news), news.name)
