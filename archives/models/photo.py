from typing import List, Any

from django.db import models

from archives.models.base_model import BaseModel
from archives.models.album import Album
from families.models import Family


class Photo(BaseModel):
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)
    photo_image = models.ImageField(upload_to="photo/", null=True, blank=True)
    like_count = models.IntegerField(default=0)
