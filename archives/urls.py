from django.urls import path

from . import views
from .views import create_read_all_album

app_name = "archives"


urlpatterns = [
    path("families/<int:family_id>/album", create_read_all_album, name="create_read_all_album"),
]

