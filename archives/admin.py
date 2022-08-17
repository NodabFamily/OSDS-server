from django.contrib import admin

from .models import Album,Comment,Like,Photo,Tag,Bookmark
# Register your models here.


@admin.register(Album)
class LikeLionModelAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','family_id','title','album_image',)
    list_editable = ('title',)

@admin.register(Comment)
class LikeLionModelAdmin(admin.ModelAdmin):
    list_display = ('id','photo_id','user_id','comment',)
    list_editable = ('comment',)

@admin.register(Like)
class LikeLionModelAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','photo_id','created_at',)

@admin.register(Photo)
class LikeLionModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'album_id', 'family_id', 'photo_image', 'like_count',)

@admin.register(Tag)
class LikeLionModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'album_id', 'family_id', 'content',)
    list_editable = ('content',)