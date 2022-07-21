from django.contrib import admin

# Register your models here.
from .models import Album, Comment, Like, Photo, Tag

admin.site.register(Album)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Photo)
admin.site.register(Tag)