from django.db import models


class Family(models.Model):
    family_name = models.CharField(max_length=31, default='', null=True)
    cover_image = models.URLField(default="https://osds-bucket.s3.ap-northeast-2.amazonaws.com/image/%EC%98%A4%EC%88%9C%EC%9D%B4.png")
    bio = models.CharField(max_length=255, default='',null=True,blank=True)
    password = models.CharField(max_length=31, default='', null=True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.family_name