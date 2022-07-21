from django.contrib import admin

# Register your models here.
from .models import Family, User

admin.site.register(Family)
admin.site.register(User)