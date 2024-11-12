from django.test import TestCase

from task_manager.forms import WorkerCreationForm, WorkerUpdateForm, NewForm
from task_manager.models import Position


class FormsTest(TestCase):
    def setUp(self):
        self.position = Position.objects.create(
            name="Test Position"
        )

    def test_worker_creation_form(self):
        form_data = {
            "username": "TestWorker",
            "first_name": "Test First",
            "last_name": "Test Last",
            "email": "some_email@mail.com",
            "password1": "TestPassword123",
            "password2": "TestPassword123",
            "position": self.position,
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_worker_update_form(self):
        form_data = {
            "username": "TestWorker",
            "first_name": "Test First",
            "last_name": "Test Last",
            "email": "some_email@mail.com",
            "position": self.position,
            "password": None,
        }
        form = WorkerUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)

    def test_new_form(self):
        form_data = {
            "name": "Some news",
            "description": "Some description",
        }
        form = NewForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data, form_data)
