from typing import List, Any

from django.db import models

from archives.models.base_model import BaseModel
from archives.models.album import Album
from families.models import Family
from accounts.models import User


class Photo(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)
    photo_image = models.URLField()
    like_count = models.IntegerField(default=0)
