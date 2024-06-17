from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name", ]

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        default=None,
        related_name="workers",
    )

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.position}: {self.last_name} {self.first_name}"

    def get_absolute_url(self):
        return reverse("task_manager:worker-detail", kwargs={"pk": self.pk})


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["name", ]

    def __str__(self):
        return self.name


class Task(models.Model):
    PRIORITY_CHOICES = {
        "H": "High",
        "M": "Medium",
        "L": "Low",
        "U": "Undefined",
    }
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    deadline = models.DateField()
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=1,
        choices=PRIORITY_CHOICES,
        default="U"
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tasks"
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="tasks"
    )

    class Meta:
        ordering = ["is_completed", "deadline", "name", ]

    def __str__(self):
        return f"{self.name} ({self.priority}) / {self.deadline}"

    def get_absolute_url(self):
        return reverse("task_manager:task-detail", kwargs={"pk": self.pk})


class New(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        Worker,
        on_delete=models.DO_NOTHING,
        related_name="news",
    )

    class Meta:
        ordering = ["-creation_date", ]

    def __str__(self):
        return self.name
