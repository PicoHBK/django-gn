from django.contrib import admin
from .models import CustomUser,Code

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Code)