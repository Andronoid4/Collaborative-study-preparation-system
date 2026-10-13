from django.urls import path

from . import views

app_name = "topics"

urlpatterns = [
    path("", views.topic_list, name="list"),
    path("<int:topic_id>/", views.topic_detail, name="detail"),
]
