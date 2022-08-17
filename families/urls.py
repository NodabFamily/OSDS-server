from django.urls import path

from . import views
from .views import create_family, check_validate_family, read_update_delete_family

app_name = "families"


urlpatterns = [
    path("families", create_family, name="create_family"),
    path("families/<int:family_id>/validate", check_validate_family, name="check_validate_family"),
    path("families/<int:family_id>", read_update_delete_family, name="read_update_delete_family"),
]