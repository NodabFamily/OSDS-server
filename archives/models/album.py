from django.db import models

from archives.models.base_model import BaseModel
from families.models import Family
from accounts.models import User

class Album(BaseModel):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=31)
    album_image = models.URLField(max_length=500, blank=True, default='')

