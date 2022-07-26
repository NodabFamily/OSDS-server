from django.contrib import admin

from .models import Album,Comment,Like,Photo,Tag
# Register your models here.

admin.site.register(Album),
admin.site.register(Comment),
admin.site.register(Like),
admin.site.register(Photo),
admin.site.register(Tag)