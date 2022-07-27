from django.db import models


class Family(models.Model):
    family_name = models.CharField(max_length=30, default='', null=True)
    cover_image = models.ImageField(upload_to='family/', null=True, blank=True)
