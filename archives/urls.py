from django.urls import path

from . import views
from .views import create_read_all_album, read_edit_delete_album

app_name = "archives"


urlpatterns = [
    path("families/<int:family_id>/album", create_read_all_album, name="create_read_all_album"),
    path("families/<int:family_id>/album/<int:album_id>", read_edit_delete_album, name="read_edit_delete_album"),
]

