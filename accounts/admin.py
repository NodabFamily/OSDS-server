from django.contrib import admin

from .models import Family, User

# Register your models here.
admin.site.register(Family),
admin.site.register(User)

