from django.db import models

from families.models import Family
from archives.models.album import Album


class Tag(models.Model):
    # album_id = models.ForeignKey(Album, on_delete=models.CASCADE, null=True, blank=True)
    album_id = models.ManyToManyField(Album)
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)
    content = models.CharField(max_length=255)

