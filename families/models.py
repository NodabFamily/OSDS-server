from django.db import models


class Family(models.Model):
    family_name = models.CharField(max_length=31, default='', null=True)
    cover_image = models.ImageField(upload_to='family/', null=True, blank=True)
    bio = models.CharField(max_length=255, default='',null=True,blank=True)
    password = models.CharField(max_length=31, default='', null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
