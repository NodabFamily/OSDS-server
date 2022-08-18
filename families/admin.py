from django.contrib import admin

# Register your models here.
from .models import Family

@admin.register(Family)
class LikeLionModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'family_name', 'cover_image', 'bio', 'created_at', 'updated_at')