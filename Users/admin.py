from django.contrib import admin

from .models import User


@admin.register(User)
class AdminRegister(admin.ModelAdmin):
    list_display = ["username", "first_name", "email"]
    search_fields = ["username", "first_name", "email"]
