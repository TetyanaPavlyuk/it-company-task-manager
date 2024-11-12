from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

from .models import Position, Worker, TaskType, Task, New


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + (
        "position",
    )
    fieldsets = UserAdmin.fieldsets + (
        (("Additional Info", {"fields": ("position", )}), )
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional Info", {
            "fields": ("position", "first_name", "last_name", )
        }), )
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_filter = ("assignees", "deadline", "priority", )
    search_fields = ("name", "description", "task_type", "assignees", )


admin.site.register(Position)
admin.site.register(TaskType)
admin.site.register(New)
admin.site.unregister(Group)
