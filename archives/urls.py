from django.urls import path

from . import views
from .views import create_read_all_album, read_edit_delete_album, delete_photo, create_comment, edit_delete_comment

app_name = "archives"


urlpatterns = [
    path("families/<int:family_id>/albums", create_read_all_album, name="create_read_all_album"),
    path("families/<int:family_id>/albums/<int:album_id>", read_edit_delete_album, name="read_edit_delete_album"),
    path("families/<int:family_id>/albums/<int:album_id>/photo/<int:photo_id>", delete_photo, name="delete_photo"),
    path("families/<int:family_id>/photos/<int:photo_id>/comments", create_comment, name="create_comment"),
    path("families/<int:family_id>/photos/<int:photo_id>/comments/<int:comment_id>", edit_delete_comment, name="edit_delete_comment")
]

