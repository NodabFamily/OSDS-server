from django.urls import path

from . import views
from .views import create_album

app_name = "archives"


urlpatterns = [
    path("families/<int:family_id>/album", create_album, name="create_album"),
]

