from django.db import models

from accounts.models.family import Family
from archives.models.album import Album


class Tag(models.Model):
    album_id = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=255)