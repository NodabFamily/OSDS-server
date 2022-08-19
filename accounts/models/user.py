from django.db import models
from django.contrib.auth.models import AbstractUser
from families.models import Family


class User(AbstractUser):
    family_id = models.ForeignKey(Family, on_delete=models.CASCADE, null=True, blank=True)
    member_id = models.CharField(max_length=31, null=True, default='')
    password = models.CharField(max_length=31, null=True, default='')
    name = models.CharField(max_length=31, null=True, default='')
    birth = models.CharField(max_length=31, null=True, default='')
    bio = models.CharField(max_length=255, null=True, default='')
    is_participant = models.BooleanField(null=False, default=False)
    avatar = models.URLField(max_length=500, blank=True, default="https://osds-bucket.s3.ap-northeast-2.amazonaws.com/image/%EC%98%A4%EC%88%9C%EC%9D%B4.png")
    nickname = models.CharField(max_length=31, null=True, default='')


