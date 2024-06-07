from django.urls import path

from .views import (
    index,
    PositionListView,
)


urlpatterns = [
    path("", index, name="index"),
    path("tasks/", PositionListView.as_view(), name="position_list"),
]

app_name = "task_manager"
