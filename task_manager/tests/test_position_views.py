from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import Position


class PublicPositionTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Test Position",
        )
        self.position.save()

        self.urls_list = [
            reverse("task_manager:position-list"),
            reverse("task_manager:position-create"),
            reverse(
                "task_manager:position-update",
                kwargs={"pk": self.position.id}
            ),
            reverse(
                "task_manager:position-delete",
                kwargs={"pk": self.position.id}
            ),
        ]

    def test_login_required(self):
        response_list = [self.client.get(url) for url in self.urls_list]
        for res in response_list:
            self.assertNotEqual(res.status_code, 200)


class PrivatePositionTest(TestCase):
    def setUp(self):
        self.position1 = Position.objects.create(
            name="Test Position",
        )
        self.position1.save()

        self.worker = get_user_model().objects.create_user(
            username="TestWorker",
            first_name="Test FirstName",
            last_name="Test LastName",
            password="TestPassword123",
            position=self.position1,
        )
        self.worker.save()

        self.client.force_login(self.worker)

        self.position2 = Position.objects.create(
            name="Other Position",
        )
        self.position2.save()

        self.urls_list = [
            reverse("task_manager:position-list"),
            reverse("task_manager:position-create"),
            reverse(
                "task_manager:position-update",
                kwargs={"pk": self.position1.id}
            ),
            reverse(
                "task_manager:position-delete",
                kwargs={"pk": self.position1.id}
            ),
        ]

        self.response_list = [self.client.get(url) for url in self.urls_list]

        self.templates_list = [
            "task_manager/position_list.html",
            "task_manager/position_form.html",
            "task_manager/position_form.html",
            "task_manager/position_confirm_delete.html",
        ]

        self.position_list_url = reverse("task_manager:position-list")
        self.position_list_response = self.client.get(
            self.position_list_url
        )

    def test_user_logged_in_required(self):
        for res in self.response_list:
            self.assertEqual(res.status_code, 200)

    def test_display_all_positions(self):
        positions = Position.objects.all()
        self.assertEqual(
            list(self.position_list_response.context["position_list"]),
            list(positions)
        )

    def test_search_position(self):
        search_position = Position.objects.filter(
            name__icontains="Test"
        )
        search_position_response = self.client.get(
            self.position_list_url + "?model=Test"
        )
        self.assertEqual(
            list(search_position),
            list(search_position_response.context["position_list"])
        )

    def test_correct_templates(self):
        for num in range(len(self.templates_list)):
            self.assertTemplateUsed(
                self.response_list[num],
                self.templates_list[num]
            )
