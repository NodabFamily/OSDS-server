from django.urls import path

from . import views
from .views import create_family

app_name = "families"


urlpatterns = [
    path("families", create_family, name="create_family"),
    # path("families/<int:family_id>/", check_password, name="check_password"),
]