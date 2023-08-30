from django.contrib import admin
from .models import Badge

# Register your models here.


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "rule", "created", "modified")
    search_fields = ("name",)
    list_filter = ("created", "modified")
