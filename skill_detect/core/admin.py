from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Domain, User


admin.site.register(Domain)
admin.site.register(User, UserAdmin)