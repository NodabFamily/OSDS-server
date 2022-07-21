from django.urls import path

from .views import create_album

urlpatterns = [
    path('create-album/<int:family_id>', create_album, name="create-album")
]