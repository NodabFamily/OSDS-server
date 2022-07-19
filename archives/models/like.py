from django.db import models

from accounts.models.user import User
from archives.models.photo import Photo

class Like(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    photo_id = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
