from django.db import models

from archives.models.base_model import BaseModel
from accounts.models.family import Family

class Album(BaseModel):
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=31)
    cover_image = models.ImageField(upload_to="album/", null=True, blank=True)

    def get_img_url(self):
        if not self.cover_image:
            return ""
        else:
            return self.cover_image.url
