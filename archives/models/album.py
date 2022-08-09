from django.db import models

from archives.models.base_model import BaseModel
from families.models import Family

class Album(BaseModel):
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=31)
    album_image = models.URLField()

