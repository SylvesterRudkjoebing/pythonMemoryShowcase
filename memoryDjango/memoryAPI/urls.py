from django.urls import path
from . import views

app_name = "memoryAPI"
urlpatterns = [
    path("", views.index, name="index"),
    path("memory", views.memory, name="memory"),
    path("<str:name>", views.greet, name="greet")
]