from django.urls import path

from . import views

from .views import read_edit_delete_user, create_user

app_name = "accounts"

urlpatterns = [
    path("users", create_user, name="create_user"),
    path("users/<int:id>", read_edit_delete_user, name ="read_edit_delete_user"),
]