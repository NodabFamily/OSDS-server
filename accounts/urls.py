from django.urls import path

from . import views

from .views import *

app_name = "accounts"

urlpatterns = [
    path("users", create_user, name="create_user"),
    path("users/<int:user_id>", read_edit_delete_user, name ="read_edit_delete_user"),
    path("users/login",login_view, name ="login"),
    path("users/logout", logout_view, name ="logout"),
]