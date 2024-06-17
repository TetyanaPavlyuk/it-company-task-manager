from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from task_manager.models import Position


class AdminSiteTests(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="testPassword123"
        )
        self.client.force_login(self.admin_user)
        self.position = Position.objects.create(name="Some position")
        self.worker = get_user_model().objects.create_user(
            username="Specialist",
            password="testPassword456",
            position=self.position
        )

    def test_worker_position_listed(self):
        """
        Test that worker's position is in list_display
        on worker admin page
        """
        url = reverse("admin:task_manager_worker_changelist")
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

    def test_worker_detail_position_listed(self):
        """
        Test that driver's license number is on driver detail admin page
        """
        url = reverse(
            "admin:task_manager_worker_change",
            args=[self.worker.id]
        )
        res = self.client.get(url)
        self.assertContains(res, self.worker.position)

    def test_worker_add_position_listed(self):
        """
        Test that driver's license number is on driver add admin page
        """
        url = reverse("admin:task_manager_worker_add")
        res = self.client.get(url)
        self.assertContains(res, "position")
