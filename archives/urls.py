from django.urls import path

from . import views
from .views import create_read_all_album, read_edit_delete_album, delete_photo, create_comment, edit_delete_comment, \
    do_undo_like, do_undo_bookmark, create_tag, read_family_photo
app_name = "archives"


urlpatterns = [
    path("families/<int:family_id>/albums", create_read_all_album, name="create_read_all_album"),
    path("families/<int:family_id>/albums/<int:album_id>", read_edit_delete_album, name="read_edit_delete_album"),
    path("families/<int:family_id>/albums/<int:album_id>/photos/<int:photo_id>", delete_photo, name="delete_photo"),
    path("families/<int:family_id>/photos/<int:photo_id>/comments", create_comment, name="create_comment"),
    path("families/<int:family_id>/photos/<int:photo_id>/comments/<int:comment_id>", edit_delete_comment, name="edit_delete_comment"),
    path("families/<int:family_id>/albums/<int:album_id>/likes/<int:photo_id>", do_undo_like, name="do_undo_like"),
    path("families/<int:family_id>/albums/<int:album_id>/bookmarks/<int:photo_id>", do_undo_bookmark, name="do_undo_bookmark"),
    path("families/<int:family_id>/albums/<int:album_id>/tags", create_tag, name="create_tag"),
    path("families/<int:family_id>/photo", read_family_photo, name=" read_family_photo")
]

