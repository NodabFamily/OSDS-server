from django.db import models

from archives.models.base_model import BaseModel
from accounts.models.user import User
from archives.models.photo import Photo


class Comment(BaseModel):
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.CharField(max_length=255, default='', null=True)

    def __str__(self):
        return self.comment

