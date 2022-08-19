from django.contrib import admin
from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.
@admin.register(User)
class LikeLionModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'family_id', 'member_id', 'name', 'bio', 'is_participant', 'nickname',)
