from django.db import models

from archives.models.base_model import BaseModel
from archives.models.album import Album
from accounts.models.family import Family


class Photo(BaseModel):
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)